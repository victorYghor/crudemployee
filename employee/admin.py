#account/admin.py

from django.contrib import admin
from .models import Employee, Department

admin.site.register(Employee)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
