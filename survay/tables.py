import django_tables2 as tables
from .models import Projects, SprDolgn, HandbookObjects, \
    VObjects, TypeStreet, ObjectsPersonals, Addresses, \
    VObjectsAddress, OneObjectsPersonals, CRMPersonals
from django.utils.html import format_html


class ProjectsTable(tables.Table):
    class Meta:
        model = Projects
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 6

    def render_ProjectName(self, value, record):
        return format_html("<a href={}>{}</a>", record.ProjectID, value)

    def value_ProjectName(self, value):
        return value

    def render_LastUpdate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_LastUpdate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")

    def render_ArhivDate(self, value):
        if value:
            return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))
        else:
            return format_html("<h5>{}</h5>", '')

    def value_ArhivDate(self, value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M")
        else:
            return ''


class SprDolgnTable(tables.Table):
    class Meta:
        model = SprDolgn
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },

        }
        per_page = 9

    def render_DolgnName(self, value, record):
        return format_html("<a href={}>{}</a>", record.SprDolgnID, value)

    def value_DolgnName(self, value):
        return value

    def render_InsertDate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_InsertDate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")


class HandbookObjectsTable(tables.Table):
    class Meta:
        model = HandbookObjects
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 9

    def render_ObjectName(self, value, record):
        return format_html("<a href={}>{}</a>", record.HandbookObjectID, value)

    def value_ObjectName(self, value):
        return value


class VObjectsTable(tables.Table):
    class Meta:
        model = VObjects
        template_name = "django_tables2/bootstrap.html"
        fields = ['ObjectID', 'title', 'full_title', 'categories', 'StatusID', 'AddressID', 'InsertDate', 'personals']
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 9

    def render_title(self, value, record):
        return format_html("<a href={}>{}</a>", record.ObjectID, value)

    def value_title(self, value):
        return value

    def render_InsertDate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_InsertDate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")

    def render_AddressID(self, value):
        w4 = Addresses.objects.get(AddressID__exact=value)
        return format_html("<h5>{}</h5>", w4)

    def value_AddressID(self, value):
        return value

    def render_personals(self, value, record):
        return format_html("<a href='search/{}'>{}</a>", record.ObjectID, value)

    def value_personals(self, value):
        return value


# Объекты по заданному адресу
class VObjectsAddressTable(tables.Table):
    class Meta:
        model = VObjectsAddress
        template_name = "django_tables2/bootstrap.html"
        fields = ['ObjectID', 'title', 'full_title', 'categories',
                  'StatusID', 'AddressID', 'InsertDate', 'personals']
        row_attrs = {
            "data-id": lambda record: [record.pk, record.AddressID],
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 9

    def render_title(self, value, record):
        return format_html("<a href={}>{}</a>", record.ObjectID, value)

    def value_title(self, value):
        return value

    def render_InsertDate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_InsertDate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")

    def render_AddressID(self, value):
        w4 = Addresses.objects.get(AddressID__exact=value)
        return format_html("<h5>{}</h5>", w4)

    def value_AddressID(self, value):
        return value

    def render_personals(self, value, record):
        return format_html("<a href='objsearch/{}'>{}</a>", record.ObjectID, value)

    def value_personals(self, value):
        return value


class TypeStreetTable(tables.Table):
    class Meta:
        model = TypeStreet
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 11

    def render_TypeStreet(self, value, record):
        return format_html("<a href={}>{}</a>", record.id, value)

    def value_TypeStreet(self, value):
        return value


# Персонал на объектах
class ObjectsPersonalsTable(tables.Table):
    class Meta:
        model = ObjectsPersonals
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 10

    def render_PersFam(self, value, record):
        return format_html("<a href={}>{}</a>", record.ObjectPersonalID, value)

    def value_PersFam(self, value):
        return value

    def render_InsertDate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_InsertDate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")


# Таблица для персонала Одного объекта
class OneObjectsPersonalsTable(tables.Table):
    class Meta:
        model = OneObjectsPersonals
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 10

    def render_PersFam(self, value, record):
        w4 = record.ObjectID.ObjectID
        return format_html("<a href='{}/{}/'>{}</a>",
                           w4,
                           record.ObjectPersonalID,
                           value)

    def value_PersFam(self, value):
        return value

    def render_InsertDate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_InsertDate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")


class AddressesTable(tables.Table):
    class Meta:
        model = Addresses
        template_name = "django_tables2/bootstrap.html"
        row_attrs = {
            "data-id": lambda record: record.pk,
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 10

    def render_Region(self, value, record):
        return format_html("<a href={}>{}</a>", record.AddressID, value)

    def value_Region(self, value):
        return value

    def render_Gis2Address(self, value, record):
        return format_html("<a href='search/{}'>{}</a>", record.AddressID, value)

    def value_Gis2Address(self, value):
        return value

    def render_InsertDate(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_InsertDate(self, value):
        return value.strftime("%Y-%m-%d %H:%M")


# Пользователи по заданной группе
class CRMPersonalsTable(tables.Table):

    class Meta:
        model = CRMPersonals
        template_name = "django_tables2/bootstrap.html"
        fields = ['id', 'username', 'last_name', 'first_name',
                  'email', 'is_active',
                  'last_login', 'date_joined',
                  'groupid',
                  ]
        row_attrs = {
            "data-id": lambda record: record.pk
        }
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend"  # Instead of `desc`
                },
            },
        }
        per_page = 10

    def render_username(self, value, record):
        return format_html("<a href='{}'>{}</a>", record.id, value)

    def value_username(self, value):
        return value

    def render_last_login(self, value):
        if value:
            end_value = value.strftime("%Y-%m-%d %H:%M")
        else:
            end_value = ''
        return format_html("<h5>{}</h5>", end_value)

    def value_last_login(self, value):
        return value.strftime("%Y-%m-%d %H:%M")

    def render_date_joined(self, value):
        return format_html("<h5>{}</h5>", value.strftime("%Y-%m-%d %H:%M"))

    def value_date_joined(self, value):
        return value.strftime("%Y-%m-%d %H:%M")
