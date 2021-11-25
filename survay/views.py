from django.db.models import Count, Value, CharField
import json
# import logging
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import requests
import time
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, FormView
import django_tables2 as tables
from django_tables2 import LazyPaginator
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
# from django_tables2.config import RequestConfig
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout


from .models import Projects, SprDolgn, \
                    HandbookObjects, VObjects, \
                    TypeStreet, ObjectsPersonals, Addresses, \
                    VObjectsAddress, OneObjectsPersonals, CRMPersonals
from .tables import ProjectsTable, SprDolgnTable, \
                    HandbookObjectsTable, VObjectsTable, \
                    TypeStreetTable, ObjectsPersonalsTable, \
                    AddressesTable, \
                    VObjectsAddressTable, OneObjectsPersonalsTable, \
                    CRMPersonalsTable
from .forms import ProjectsForm, SprDolgnForm, \
                    HandbookObjectsForm, VObjectsForm, \
                    TypeStreetForm, ObjectsPersonalsForm, AddressesForm, \
                    VObjectsAddressForm, OneObjectsPersonalsForm, \
                    CRMPersonalsForm, CRMPersonalsCreationForm, CRMPersonalsPassChangeForm
from .filters import SprDolgnFilter, VObjectsFilter, \
                    ObjectsPersonalsFilter, AddressesFilter, CRMPersonalsFilter
from .utils import *
from adjsite.settings.basesettings import API_URL, API_KEY_GEO


def index(request):
    # на начальной странице - проверка на вход для ранее залогинившегося пользователя
    # всегда требует логин - при повторном входе -сброс  через отключение логина
    if request.user.is_authenticated:
        logout(request)
    return render(request, "survay/index.html")


def mainindex(request):
    return render(request, "survay/survaybase.html")


# обращение к Геолокатору Яндекс. Требуется apikey - зарегистрировать в Яндекс заранее!
def external_view(request):
    api_url = API_URL
    city = request.POST.get("address")

    params = {
        'apikey': API_KEY_GEO,
        'format': 'json',
        'geocode': city,
    }
    attempt_num = 0  # счетчик повтора попыток запросов к Геолокатору
    while attempt_num < 5:
        res = requests.get(api_url, params=params)

        if res.status_code == 200:
            # data = res.json()
            data = json.loads(res.text)
            data2 = data.get('response').get('GeoObjectCollection').get('featureMember')
            # из списка - отбор нужных данных
            # new_data1 = []
            new_data2 = []
            counter = 0
            for el in data2:
                geopoint = el.get('GeoObject').get('Point').get('pos')
                geoobj = el.get('GeoObject').get('metaDataProperty').get('GeocoderMetaData')
                adrstr = geoobj.get('text')
                adrdict = geoobj.get('AddressDetails').get('Country')
                counter += 1
                new_data2.append((counter, adrstr, adrdict, geopoint))

            t1 = loader.get_template("survay/adress_form.html")

            return HttpResponse(t1.render(context={'res_text': new_data2,
                                                   'res_status': res.status_code,
                                                   'url_name': 'adr_find_page',
                                                   }))
        else:
            attempt_num += 1
            time.sleep(5)
    return HttpResponse(b'error: "Request failed"')


# парсинг ответа Геолокатора - добавление адреса
@csrf_exempt
def external_address_create(request):
    res = request.POST.get("_selected_action")
    res2 = res.split(';')
    data2 = res2[1]
    # из списка - отбор нужных данных
    if isinstance(data2, str):
        list_geo = data2.split()
        shir = list_geo[0]
        dolg = list_geo[1]
    else:
        shir = 0
        dolg = 0

    data = res2[2].replace("\'", "\"")
    # rr2 = type(data)
    geoobj = json.loads(data)
    adrstr = geoobj.get('AddressLine')
    adrdictlist = geoobj.get('AdministrativeArea')

    region_1 = adrdictlist.get('AdministrativeAreaName')

    reg_2 = adrdictlist.get('SubAdministrativeArea')
    if isinstance(reg_2, dict):
        region_2 = reg_2.get('SubAdministrativeAreaName')
        # Locality внутри SubAdministrativeArea
        city_0 = reg_2.get('Locality')
    else:
        region_2 = '-'
        # Locality внутри AdministrativeArea
        city_0 = adrdictlist.get('Locality')

    if isinstance(city_0, dict):
        city_1 = city_0.get('LocalityName')
        dopreg_0 = city_0.get('DependentLocality')
        if isinstance(dopreg_0, dict):
            dopreg_1 = dopreg_0.get('DependentLocalityName')
        else:
            dopreg_1 = '-'

        if isinstance(dopreg_0, dict):
            # 2-е DependentLocality:
            dopreg_10 = dopreg_0.get('DependentLocality')
            if isinstance(dopreg_10, dict):
                dopreg_11 = dopreg_10.get('DependentLocalityName')
            else:
                dopreg_11 = ''
        else:
            dopreg_10 = dopreg_0
            dopreg_11 = '-'

        if dopreg_1 == '-':
            city_10 = city_0
            street_0 = city_0.get('Thoroughfare')
        elif dopreg_11 == '':
            city_10 = dopreg_0
            street_0 = dopreg_0.get('Thoroughfare')
        else:
            city_10 = dopreg_10
            street_0 = dopreg_10.get('Thoroughfare')

        if isinstance(street_0, dict):
            street_1 = street_0.get('ThoroughfareName')
            house_0 = street_0.get('Premise')
        else:
            street_1 = '-'
            house_0 = city_10.get('Premise')

        if isinstance(house_0, dict):
            if isinstance(house_0.get('PremiseNumber'), dict):
                house_2 = house_0.get('PremiseNumber')
            elif isinstance(house_0.get('PremiseNumber'), str):
                house_2 = house_0.get('PremiseNumber')
            else:
                house_2 = ''
            if isinstance(house_0.get('PremiseName'), dict):
                house_1 = house_0.get('PremiseName')
            elif isinstance(house_0.get('PremiseName'), str):
                house_1 = house_0.get('PremiseName')
            else:
                house_1 = ''
        else:
            house_1 = '-'
            house_2 = ''

        house_3 = ' '.join([house_1, house_2])

        Addresses.objects.create(
            Region=region_1,
            SubRegion=region_2,
            city=city_1,
            Raion=dopreg_1,
            street=street_1,
            typestreet='улица',
            house=house_3,
            latitude=shir,
            longitude=dolg,
            Gis2Address=adrstr,
        )
    return HttpResponseRedirect(reverse('addresses_list'))
    # return HttpResponse(b'Good. Record was added.',)


# страница для ввода поисковой строки адреса
def external_api_view(request):
    pp = request.user.has_perm('survay.add_addresses')
    if not pp:
        raise PermissionDenied()
    return render(request,
                  "survay/adressfind_form.html",
                  context={'url_name': 'main_page', }
                  )


# Список Рабочих проектов с "техничкой" - для админимтраторов CRM:
class ProjectsList(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ('survay.view_projects')
    model = Projects
    table_class = ProjectsTable
    queryset = Projects.objects.all().order_by("ProjectName")
    paginator_class = LazyPaginator
    template_name = "survay/simple_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Cписок проектов'
        context['url_name_create'] = 'projects_create'
        return context


class ProjectsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_projects')
    model = Projects
    fields = '__all__'


class ProjectsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_projects')
    model = Projects
    form_class = ProjectsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('projects_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новый проект'
        context['url_name'] = 'projects_list'
        return context


class ProjectsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_projects')
    model = Projects
    # fields = ['username', 'disc', 'is_active', 'uservid']
    form_class = ProjectsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('projects_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Проект:'
        context['url_name'] = 'projects_list'
        return context


class FilteredSprDolgnList(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = ('survay.view_sprdolgn')
    model = SprDolgn
    queryset = SprDolgn.objects.all().order_by("SprDolgnID")
    table_class = SprDolgnTable
    paginator_class = LazyPaginator
    filterset_class = SprDolgnFilter
    template_name = "survay/simple_list.html"
    export_name = 'export_sprdolgn'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Справочник должностей'
        context['url_name_create'] = 'sprdolgn_create'
        context['export'] = 'xlsx'
        return context


class SprDolgnDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_sprdolgn')
    model = SprDolgn
    fields = '__all__'


class SprDolgnCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_sprdolgn')
    model = SprDolgn
    form_class = SprDolgnForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('sprdolgn_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новая должность (специалист) : '
        context['url_name'] = 'sprdolgn_list'
        return context


class SprDolgnUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_sprdolgn')
    model = SprDolgn
    form_class = SprDolgnForm
    template_name = "survay/projects_form.html"

    def get_success_url(self):
        return reverse_lazy('sprdolgn_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Должность (специалист) : '
        context['url_name'] = 'sprdolgn_list'
        # context['url_del_name'] = 'sprdolgn_delete'
        return context


class HandbookObjectsList(PermissionRequiredMixin, ExportMixin, tables.SingleTableView):
    permission_required = ('survay.view_handbookobjects')
    model = HandbookObjects
    table_class = HandbookObjectsTable
    queryset = HandbookObjects.objects.all().order_by("ObjectName")
    paginator_class = LazyPaginator
    template_name = "survay/simple_list.html"
    export_name = 'export_handbookobjects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Справочник типов объектов'
        context['url_name_create'] = 'handbookobjects_create'
        context['export'] = 'xlsx'
        return context


class HandbookObjectsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_handbookobjects')
    model = HandbookObjects
    fields = '__all__'


class HandbookObjectsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_handbookobjects')
    model = HandbookObjects
    form_class = HandbookObjectsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('handbookobjects_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новый тип объекта : '
        context['url_name'] = 'handbookobjects_list'
        return context


class HandbookObjectsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_handbookobjects')
    model = HandbookObjects
    form_class = HandbookObjectsForm
    template_name = "survay/projects_form.html"

    def get_success_url(self):
        return reverse_lazy('handbookobjects_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Тип объекта : '
        context['url_name'] = 'handbookobjects_list'
        # context['url_del_name'] = 'handbookobjects_delete'
        return context


# Список Объектов - все (модель VObjects)
class FilteredObjectsList(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = ('survay.view_vobjects')
    model = VObjects
    queryset = VObjects.objects.annotate(personals=Count('vobjects')).order_by('-ObjectID')
    table_class = VObjectsTable
    paginator_class = LazyPaginator
    filterset_class = VObjectsFilter
    template_name = "survay/simple_list.html"
    export_name = 'export_objects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Справочник объектов'
        context['url_name_create'] = 'objects_create'
        context['export'] = 'xlsx'
        context['filter_btn'] = 'filter_show'
        return context


# Список объектов по заданному адресу
class FilteredObjectsAddressList(PermissionRequiredMixin, ExportMixin, tables.SingleTableView):
    permission_required = ('survay.view_vobjects')
    model = VObjectsAddress
    # queryset = VObjectsAddress.objects.all()
    table_class = VObjectsAddressTable
    paginator_class = LazyPaginator
    template_name = "survay/simple_list.html"
    export_name = 'export_objectsaddress'

    def get_queryset(self):  # берем оригинальный queryset()
        qs = super().get_queryset()
        # и расширяем его - фильтром по AddressID
        qs2 = qs.filter(AddressID__exact=self.kwargs['addrid'])
        object_list = qs2.annotate(personals=Count('vobjects'))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = f'Справочник объектов по адресу: {self.kwargs["addrid"]}'
        context['url_name_create'] = 'search_objects_create'
        context['filter_name'] = f'{self.kwargs["addrid"]}'
        context['export'] = 'xlsx'
        return context


class ObjectsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_vobjects')
    model = VObjects
    fields = '__all__'


# Добавление записи в базу Objects (модель VObjects)
class ObjectsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_vobjects')
    model = VObjects
    form_class = VObjectsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('objects_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новый объект : '
        context['url_name'] = 'objects_list'
        return context


# Добавление в базу Objects с заданным адресом (модель proxy VObjectsAddress)
class ObjectsAddressCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_vobjects')
    model = VObjectsAddress
    form_class = VObjectsAddressForm
    template_name = "survay/projects_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial['AddressID'] = self.kwargs['addrid']
        return initial

    def get_context_data(self, *, object_list=None, **kwargs):
        addrid = self.kwargs['addrid']
        context = super().get_context_data(**kwargs)
        context['title_list'] = f'Новый объект : по адресу ({addrid})'
        context['url_name'] = 'search_objects'
        context['filter_name'] = addrid
        return context


class ObjectsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('survay.delete_vobjects')
    model = VObjects
    success_url = reverse_lazy('objects_list')


# Изменение записи в базе Objects (модель VObjects)
class ObjectsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_vobjects')
    model = VObjects
    form_class = VObjectsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('objects_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Описание объекта : '
        context['url_name'] = 'objects_list'
        context['url_del_name'] = 'objects_delete'
        return context


# Изменение записи в базе Objects с фильтром (модель VObjectsAddress)
class ObjectsAddressUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_vobjects')
    model = VObjectsAddress
    form_class = VObjectsAddressForm
    template_name = "survay/projects_form.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        addrid = self.kwargs['addrid']
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Описание объекта по адресу : '
        context['url_name'] = 'search_objects'
        context['filter_name'] = addrid
        # context['url_del_name'] = 'objects_delete'
        return context


class TypeStreetList(PermissionRequiredMixin, tables.SingleTableView):
    permission_required = ('survay.view_typestreet')
    model = TypeStreet
    table_class = TypeStreetTable
    queryset = TypeStreet.objects.all().order_by("TypeStreet")
    paginator_class = LazyPaginator
    template_name = "survay/simple_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Справочник типов улиц'
        context['url_name_create'] = 'typestreet_create'
        return context


class TypeStreetCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_typestreet')
    model = TypeStreet
    form_class = TypeStreetForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('typestreet_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новый тип улиц : '
        context['url_name'] = 'typestreet_list'
        return context


class TypeStreetDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_typestreet')
    model = TypeStreet
    fields = '__all__'


class TypeStreetUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_objects')
    model = TypeStreet
    form_class = TypeStreetForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('typestreet_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Наименование : '
        context['url_name'] = 'typestreet_list'
        # context['url_del_name'] = 'typestreet_list'
        return context


# Персонал объектов - полный список
class FilteredObjectsPersonalsList(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = ('survay.view_objectspersonals')
    model = ObjectsPersonals
    queryset = ObjectsPersonals.objects.all().order_by("ObjectID")
    table_class = ObjectsPersonalsTable
    paginator_class = LazyPaginator
    filterset_class = ObjectsPersonalsFilter
    template_name = "survay/simple_list.html"
    export_name = 'export_objectspersonals'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Справочник персонала объектов'
        context['url_name_create'] = 'objectspersonals_create'
        context['export'] = 'xlsx'
        context['filter_btn'] = 'filter_show'
        return context


# Персонал одного объекта - список с фильтром по ObjectID
class FilteredOneObjectsPersonalsList(PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = ('survay.view_objectspersonals')
    model = OneObjectsPersonals
    table_class = OneObjectsPersonalsTable
    paginator_class = LazyPaginator
    filterset_class = ObjectsPersonalsFilter
    template_name = "survay/simple_list.html"
    export_name = "export_oneobjectspersonals"

    def get_queryset(self):  # берем оригинальный queryset()
        qs = super().get_queryset()
        # и расширяем его - фильтром по ObjectID
        object_list = qs.filter(ObjectID__exact=self.kwargs['objid'])
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        objid = self.kwargs["objid"]
        context = super().get_context_data(**kwargs)
        context['title_list'] = f'Справочник персонала объекта ({objid})'
        context['filter_name'] = objid
        context['url_name_create'] = 'search_personals_create'
        context['export'] = 'xlsx'
        context['filter_btn'] = 'filter_show'
        return context


class OneObjectsPersonalsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_objectspersonals')
    model = OneObjectsPersonals
    fields = '__all__'


# Создание записи персонала объекта в общем списке
class ObjectsPersonalsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_objectspersonals')
    model = ObjectsPersonals
    form_class = ObjectsPersonalsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('objectspersonals_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новый сотрудник'
        context['url_name'] = 'objectspersonals_list'
        return context


# Создание записи персонала Одного объекта
class OneObjectsPersonalsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_objectspersonals')
    model = OneObjectsPersonals
    form_class = OneObjectsPersonalsForm
    template_name = "survay/projects_form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial['ObjectID'] = self.kwargs['objid']
        return initial

    def get_context_data(self, *, object_list=None, **kwargs):
        objid = self.kwargs['objid']
        context = super().get_context_data(**kwargs)
        context['title_list'] = f'Новый персонал : по объекту ({objid})'
        context['url_name'] = 'search_personals'
        context['filter_name'] = objid
        return context


class ObjectsPersonalsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_objectspersonals')
    model = ObjectsPersonals
    form_class = ObjectsPersonalsForm
    template_name = "survay/projects_form.html"
    fields = '__all__'


class ObjectsPersonalsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('survay.delete_objectspersonals')
    model = ObjectsPersonals
    success_url = reverse_lazy('objectspersonals_list')


# Редактирование записи персонала объектов (общий список)
class ObjectsPersonalsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_objectspersonals')
    model = ObjectsPersonals
    form_class = ObjectsPersonalsForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('objectspersonals_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Персонал объекта:'
        context['url_name'] = 'objectspersonals_list'
        context['url_del_name'] = 'objectspersonals_delete'
        return context


# Редактирование записи персонала Одного объекта
class OneObjectsPersonalsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_objectspersonals')
    model = OneObjectsPersonals
    form_class = OneObjectsPersonalsForm
    template_name = "survay/projects_form.html"
    # success_url = reverse_lazy('search_personals')

    def get_context_data(self, *, object_list=None, **kwargs):
        objid = self.kwargs['objid']
        context = super().get_context_data(**kwargs)
        context['title_list'] = f'Персонал одного объекта ({objid}):'
        context['url_name'] = 'search_personals'
        context['filter_name'] = objid
        # context['url_del_name'] = 'objectspersonals_delete'
        return context


# Список адресов общий (модель Addresses) + ExportMixin
class FilteredAddressesList(PermissionRequiredMixin, ExportMixin, SingleTableMixin, FilterView):
    permission_required = ('survay.view_addresses')
    model = Addresses
    queryset = Addresses.objects.all().order_by("-AddressID")
    table_class = AddressesTable
    paginator_class = LazyPaginator
    template_name = "survay/simple_list.html"
    filterset_class = AddressesFilter
    context_filter_name = 'filter'
    export_name = "export_addresses"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Справочник адресов объектов'
        context['url_name_create'] = 'adr_find_page'
        context['export'] = 'xlsx'
        context['filter_btn'] = 'filter_show'
        return context


class AddressesDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('survay.view_addresses')
    model = Addresses
    fields = '__all__'


class AddressesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('survay.add_addresses')
    model = Addresses
    form_class = AddressesForm
    template_name = "survay/projects_form.html"
    success_url = reverse_lazy('addresses_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Новый адрес'
        context['url_name'] = 'addresses_list'
        return context


class AddressesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('survay.delete_addresses')
    model = Addresses
    success_url = reverse_lazy('addresses_list')


class AddressesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('survay.change_addresses')
    model = Addresses
    form_class = AddressesForm
    template_name = "survay/projects_form.html"

    def get_success_url(self):
        return reverse_lazy('addresses_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_list'] = 'Адрес объекта:'
        context['url_name'] = 'addresses_list'
        context['url_del_name'] = 'addresses_delete'
        return context


def my_custom_permission_denied_view(request, exception):
    return render(request, 'survay/403.html')


# Список пользователей для администраторов CRM:
class CRMPersonalsList(PermissionRequiredMixin,  ExportMixin, DataMixin, SingleTableMixin, FilterView):
    permission_required = ('auth.view_user')
    model = CRMPersonals
    table_class = CRMPersonalsTable

    paginator_class = LazyPaginator
    template_name = "survay/simple_list.html"
    filterset_class = CRMPersonalsFilter
    export_name = "export_crmpersonals"

    def get_queryset(self):
        qs = super().get_queryset()
        # и расширяем его - фильтром по группе

        if self.kwargs['groupid']:
            groups = self.kwargs['groupid']
            gr = self.get_groupid_context(groups)
            object_list = qs.filter(groups__exact=gr).\
                annotate(groupid=Value(gr, output_field=CharField()))
        else:
            object_list = qs.annotate(groupid=Value(1, output_field=CharField()))

        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['groupid']:
            groups = self.kwargs['groupid']
            gr = self.get_groupid_context(groups)
            context['filter_name'] = gr
        context['title_list'] = f'Справочник СРМ персонала'
        context['url_name_create'] = 'crmpersonals_create'
        context['export'] = 'xlsx'
        context['filter_btn'] = 'filter_show'
        return context


class CRMPersonalsUpdate(PermissionRequiredMixin, DataMixin, UpdateView):
    permission_required = ('auth.change_user')
    model = CRMPersonals
    form_class = CRMPersonalsForm
    template_name = "survay/projects_form.html"

    def get_success_url(self):
        gr = self.kwargs["groupid"]
        return reverse_lazy('crmpersonals_list', kwargs={"groupid": gr})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['groupid']:
            groups = self.kwargs['groupid']
            gr = self.get_groupid_context(groups)
            context['filter_name'] = gr
        context['change_pass'] = 'crmpersonals_pass_change'
        context['title_list'] = 'Пользователь :'
        context['url_name'] = 'crmpersonals_list'
        # context['url_del_name'] = 'addresses_delete'
        return context


class CRMPersonalsCreate(PermissionRequiredMixin, DataMixin, CreateView):
    permission_required = ('auth.add_user')
    model = CRMPersonals
    form_class = CRMPersonalsCreationForm
    template_name = "survay/register.html"

    def form_valid(self, form):
        user1 = form.save()
        # После создания пользователь должен войти в группу 1 - CRM_users или 2 -CRM_staffs
        groups = self.kwargs['groupid']
        gr = self.get_groupid_context(groups)
        my_custom_sql(user1, groupid=gr)
        return super().form_valid(form)

    def get_success_url(self):
        gr = self.kwargs["groupid"]
        return reverse_lazy('crmpersonals_list', kwargs={"groupid": gr})


class CRMPersonalsDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('auth.view_user')
    model = CRMPersonals
    form_class = CRMPersonalsForm
    template_name = "survay/userlog_detail.html"
    fields = '__all__'


# Изменение пароля пользователям СРМ от имени менеджеров или админов
class CRMPersonalsPassChangeView(PermissionRequiredMixin, FormView):
    permission_required = ('auth.add_user')
    form_class = CRMPersonalsPassChangeForm
    template_name = 'survay/userpassword_change.html'

    def get_success_url(self):
        gr = self.kwargs["groupid"]
        return reverse_lazy('crmpersonals_list', kwargs={"groupid": gr})

    def get_initial(self):
        initial = super(CRMPersonalsPassChangeView, self).get_initial()
        userid = self.kwargs['pk']
        user_n = CRMPersonals.objects.get(id=userid)
        initial['username'] = user_n.username
        initial['email1'] = user_n.email
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        userid = self.kwargs['pk']
        kwargs['user'] = CRMPersonals.objects.get(id=userid)
        return kwargs

    def form_valid(self, form):
        form.save()
        # если пользователь Активен, то отправить ему сообщение
        if form.user:
            if form.user.is_active:
                form.send_email()
        return super().form_valid(form)
