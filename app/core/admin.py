from django.contrib import admin
from core import models


class StoreAdmin(admin.ModelAdmin):
    readonly_fields = ['created',]


# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Store, StoreAdmin)
