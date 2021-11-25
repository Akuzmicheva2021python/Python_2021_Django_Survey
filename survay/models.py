from django.db import models
# from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission, UserManager
from django.urls import reverse
from django.core.validators import RegexValidator


# Create your models here.
class HandbookObjects(models.Model):
    HandbookObjectID = models.AutoField(
                    verbose_name='HandbookObjectID',
                    primary_key=True,
                    blank=False,
                    null=False,
                    )
    ObjectName = models.CharField(
                    verbose_name='Наименование',
                    max_length=50,
                    blank=True,
                    null=True,
                    help_text='Наименование типов объектов: поликлиника, аптека и т.п.',
                    validators=[RegexValidator('^[a-zA-Zа-яА-Я-_ ]+$',
                                                'Разрешено использовать только буквы, пробел и дефис.',
                                                code='invalid_objectname'), ],
    )

    def __str__(self):
        return f'{self.ObjectName}'

    class Meta:
        db_table = 'HandbookObjects'
        verbose_name = "Типы объектов"
        verbose_name_plural = "Типы объектов"


class SprDolgn(models.Model):
    SprDolgnID = models.AutoField(
                    verbose_name='SprDolgnID',
                    primary_key=True,
                    blank=False,
                    null=False,
                    )
    DolgnName = models.CharField(
                    verbose_name='Наименование',
                    max_length=100,
                    blank=True,
                    null=True,
                    help_text='Наименование должностей или специальностей: провизор, врач-ревматолог и т.п.',
                    validators=[RegexValidator('^[a-zA-Zа-яА-Я-_ ]+$',
                                   'Разрешено использовать только буквы, пробел и дефис.',
                                   code='invalid_doljname'), ],
    )
    HandbookObjectID = models.ForeignKey(
        HandbookObjects,
        db_column='HandbookObjectID',
        on_delete=models.PROTECT,
        related_name='handbookobjects',
        verbose_name='Код типа объекта',
        null=False,
    )
    InsertDate = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )
    # InsertDate в базе Postgresql не получаете defaul-значения?? Вручную дописать??

    def __str__(self):
        return f'{self.DolgnName}'

    class Meta:
        db_table = 'SprDolgn'
        verbose_name = "Справочник-Должности"
        verbose_name_plural = "Должности"


# Таблица Projects
class Projects(models.Model):
    ProjectID = models.AutoField(
                    verbose_name='ProjectID',
                    primary_key=True,
                    blank=False,
                    null=False,
    )
    ProjectName = models.CharField(
        verbose_name='Название проекта',
        max_length=150,
        blank=False,
        null=False,
        validators=[RegexValidator('^[a-zA-Zа-яА-Я-0-9_ ]+$',
                                   'Разрешено использовать только буквы,цифры,пробел и дефис.',
                                   code='invalid_doljname'), ],
    )
    ProjectDesc = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,

    )
    isActive = models.PositiveSmallIntegerField(
        verbose_name='Активный',
        null=False,
        default=0,
    )
    LastUpdate = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
        null=False,
    )
    RemoteVisit = models.PositiveSmallIntegerField(
        verbose_name='Удаленные визиты',
        null=False,
        default=0,
    )
    VizitTime = models.PositiveSmallIntegerField(
        verbose_name='Время визитов',
        blank=True,
        null=True,
    )
    NoGeo = models.PositiveSmallIntegerField(
        verbose_name='Гео-локация',
        null=False,
    )
    isNewObj = models.PositiveSmallIntegerField(
        verbose_name='isNewObj',
        blank=True,
        null=True,
    )
    ArhivDate = models.DateTimeField(
        verbose_name='Дата блокировки',
        blank=True,
        null=True,
    )
    PocketName = models.CharField(
        verbose_name='Имя пакета',
        max_length=50,
        blank=True,
        null=True,
    )
    VersionNumber = models.PositiveIntegerField(
        verbose_name='VersionNumber',
        blank=True,
        null=True,
    )
    PocketSize = models.PositiveIntegerField(
        verbose_name='Размер пакета',
        blank=True,
        null=True,
    )
    WEB = models.PositiveSmallIntegerField(
        verbose_name='WEB',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.ProjectName}'

    def get_absolute_url(self):
        return reverse('projects_update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'Projects'
        verbose_name = "Проекты"
        verbose_name_plural = "Проекты"


# Таблица Objects - все
class VObjects(models.Model):
    ObjectID = models.AutoField(
                    verbose_name='ObjectID',
                    primary_key=True,
                    blank=False,
                    null=False,
    )
    title = models.CharField(
        verbose_name='Название объекта',
        max_length=255,
        blank=True,
        null=True,
    )
    full_title = models.CharField(
        verbose_name='Полное наименовае объекта',
        max_length=255,
        blank=True,
        null=True,
    )
    categories = models.CharField(
        verbose_name='Категория',
        max_length=50,
        blank=False,
        null=False,
    )
    StatusID = models.SmallIntegerField(
        verbose_name='Статус',
        blank=False,
        null=False,
        default=0,
    )
    AddressID = models.PositiveBigIntegerField(
        verbose_name='Адрес',
        blank=True,
        null=True,
    )
    InsertDate = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )
    # InsertDate в базе Postgresql не получаете defaul-значения?? Вручную дописать??

    def __str__(self):
        return f'{self.title} ({self.ObjectID})'

    def get_absolute_url(self):
        return reverse('objects_update', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'Objects'
        verbose_name = "Объекты"
        verbose_name_plural = "Объекты"


# proxy-модель для Объектов по выбранному адресу
class VObjectsAddress(VObjects):

    def get_absolute_url(self):
        return reverse('search_objects_update',
                       kwargs={'pk': self.pk, 'addrid': self.AddressID})

    class Meta:
        proxy = True
        verbose_name = "Объекты по адресу"
        verbose_name_plural = "Объекты по адресу"


class TypeStreet(models.Model):
    TypeStreet = models.CharField(
                    verbose_name='Наименование',
                    max_length=50,
                    blank=True,
                    null=True,
                    help_text='Наименование типов: улица, переулок и т.п.',
                    validators=[RegexValidator('^[a-zA-Zа-яА-Я-_ ]+$',
                                                'Разрешено использовать только буквы, пробел и дефис.',
                                                code='invalid_typestreet'), ],
    )

    def __str__(self):
        return f'{self.TypeStreet}'

    class Meta:
        db_table = 'TypeStreet'
        verbose_name = "Типы улиц"
        verbose_name_plural = "Типы улиц"

# Модель для персонала объектов (общая)
class ObjectsPersonals(models.Model):
    ObjectPersonalID = models.AutoField(
        verbose_name='ObjectPersonalID',
        primary_key=True,
        blank=False,
        null=False,
    )
    ObjectID = models.ForeignKey(
        VObjects,
        db_column='ObjectID',
        on_delete=models.PROTECT,
        related_name='vobjects',
        verbose_name='Объект',
        null=False,
    )
    PersFam = models.CharField(
        verbose_name='Фамилия',
        max_length=100,
        blank=True,
        null=True,
    )
    PersName = models.CharField(
        verbose_name='Имя',
        max_length=100,
        blank=True,
        null=True,
    )
    PersLName = models.CharField(
        verbose_name='Отчество',
        max_length=100,
        blank=True,
        null=True,
    )
    SprDolgnID = models.ForeignKey(
        SprDolgn,
        db_column='SprDolgnID',
        on_delete=models.PROTECT,
        related_name='sprdolgn',
        verbose_name='Должность',
        null=False,
    )
    PersPhone = models.CharField(
        verbose_name='Телефон',
        max_length=50,
        blank=True,
        null=True,
    )
    PersEmail = models.EmailField(
        verbose_name='Адрес Е-почты',
        max_length=100,
        blank=True,
        null=True,
    )
    Comments = models.CharField(
        verbose_name='Комментарий',
        max_length=500,
        blank=True,
        null=True,
    )
    StatusID = models.SmallIntegerField(
        verbose_name='Статус',
        blank=False,
        null=False,
        default=0,
    )
    InsertDate = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    def get_absolute_url(self):
        return reverse('personals_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.PersFam} {self.PersName} {self.PersLName} ({self.pk})'

    class Meta:
        db_table = 'ObjectsPersonals'
        verbose_name = "Персонал объектов"
        verbose_name_plural = "Персонал"


# proxy-модель для персонала Одного Объекта
class OneObjectsPersonals(ObjectsPersonals):

    def get_absolute_url(self):
        return reverse('search_personals_update',
                       kwargs={'pk': self.pk, 'objid': self.ObjectID.ObjectID})

    class Meta:
        proxy = True
        verbose_name = "Персонал объектов"
        verbose_name_plural = "Персонал объекта"


# proxy-модель для персонала Одного Объекта по выбранному адресу
class OneObjectsAddressPersonals(ObjectsPersonals):

    def get_absolute_url(self):
        return reverse('search_personals_update',
                       kwargs={'pk': self.pk,
                               'objid': self.ObjectID.ObjectID,
                               })

    class Meta:
        proxy = True
        verbose_name = "Персонал объектов"
        verbose_name_plural = "Персонал объекта"


# Таблица Addresses - all
class Addresses(models.Model):
    AddressID = models.BigAutoField(
        verbose_name='AddressID',
        primary_key=True,
        blank=False,
        null=False,
    )
    Region = models.CharField(
        verbose_name='Регион',
        max_length=255,
        blank=True,
        null=True,
    )
    SubRegion = models.CharField(
        verbose_name='Под-Регион',
        max_length=255,
        blank=True,
        null=True,
    )
    city = models.CharField(
        verbose_name='Город (Населенный пункт)',
        max_length=255,
        blank=True,
        null=True,
    )
    Raion = models.CharField(
        verbose_name='Район',
        max_length=255,
        blank=True,
        null=True,
    )
    street = models.CharField(
        verbose_name='Улица',
        max_length=255,
        blank=True,
        null=True,
    )
    typestreet = models.CharField(
        verbose_name='Тип улицы',
        max_length=50,
        blank=True,
        null=True,
    )
    house = models.CharField(
        verbose_name='Дом',
        max_length=255,
        blank=True,
        null=True,
    )
    latitude = models.FloatField(
        verbose_name='Широта',
        blank=True,
        null=True,
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
        blank=True,
        null=True,
    )
    Gis2Address = models.CharField(
        verbose_name='Адрес - строка',
        max_length=300,
        blank=True,
        null=True,
    )
    InsertDate = models.DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    def __str__(self):
        return f'{self.Gis2Address} ({self.AddressID})'

    class Meta:
        db_table = 'Addresses'
        verbose_name = "Адреса объектов"
        verbose_name_plural = "Адреса"


class CRMPersonalsManager(UserManager):
    def get_queryset(self):
        return super(CRMPersonalsManager, self).get_queryset()


# proxy-модель для пользователей и менеджеров
class CRMPersonals(User):
    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.groupid}) '

    def get_absolute_url(self):
        # gg = self.objects.groupid
        gg = self.kwargs['groupid']
        return reverse('crmpersonals_list',
                       kwargs={'groupid': gg},
                    )

    class Meta:
        proxy = True
        verbose_name = "СРМ Персонал"
        verbose_name_plural = "СРМ персонал"


