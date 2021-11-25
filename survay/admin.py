from django.contrib import admin
from .models import Projects, VObjects, TypeStreet, ObjectsPersonals, \
    Addresses, HandbookObjects, SprDolgn


# Register your models here.
admin.site.register(Projects)
admin.site.register(VObjects)
admin.site.register(TypeStreet)
admin.site.register(ObjectsPersonals)
admin.site.register(Addresses)
admin.site.register(HandbookObjects)
admin.site.register(SprDolgn)