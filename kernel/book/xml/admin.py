from django.contrib import admin
from .models import *


class ImportLogItemInline(admin.TabularInline):

    model = ImportLogItem
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ImportLogAdmin(admin.ModelAdmin):

    class Meta:
        model = Import

    inlines = [ImportLogItemInline]

    def has_add_permission(self, request):
        return False


admin.site.register(Import, ImportLogAdmin)

