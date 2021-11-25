import django_filters

from .models import SprDolgn, VObjects, ObjectsPersonals, Addresses, CRMPersonals


class SprDolgnFilter(django_filters.FilterSet):
    class Meta:
        model = SprDolgn
        fields = {
            'DolgnName': ['icontains'],
            'HandbookObjectID': ['exact'],
            'InsertDate': ['contains', 'date'],
        }


class VObjectsFilter(django_filters.FilterSet):
    class Meta:
        model = VObjects
        fields = {
            'title': ['icontains'],
            'full_title': ['icontains'],
            'categories': ['icontains'],
            'StatusID': ['exact'],
            'AddressID': ['exact'],
            'InsertDate': ['contains', 'date'],
        }


class ObjectsPersonalsFilter(django_filters.FilterSet):
    class Meta:
        model = ObjectsPersonals
        fields = {
            'PersFam': ['icontains'],
            'PersName': ['icontains'],
            'PersLName': ['icontains'],
            'PersPhone': ['icontains'],
            'PersEmail': ['icontains'],
            'Comments': ['icontains'],
            'StatusID': ['exact'],
            'ObjectID': ['exact'],
            'SprDolgnID': ['exact'],
            'InsertDate': ['contains', 'date'],
        }


class AddressesFilter(django_filters.FilterSet):
    class Meta:
        model = Addresses
        fields = {
            'Region': ['icontains'],
            'SubRegion': ['icontains'],
            'city': ['icontains'],
            'Raion': ['icontains'],
            'street': ['icontains'],
            'typestreet': ['icontains'],
            'house': ['icontains'],
            'latitude': ['exact'],
            'longitude': ['exact'],
            'Gis2Address': ['icontains'],
            'InsertDate': ['contains', 'date'],
        }


class CRMPersonalsFilter(django_filters.FilterSet):
    class Meta:
        model = CRMPersonals
        fields = {
            'username': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'email': ['icontains'],
            'is_active': ['exact'],
            'last_login': ['contains', 'date'],
            'date_joined': ['contains', 'date'],
        }