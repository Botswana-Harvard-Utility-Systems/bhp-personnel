from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from ..admin_site import bhp_personnel_admin
from ..forms import DepartmentForm
from ..models import Department
from .modeladmin_mixins import ModelAdminMixin


@admin.register(Department, site=bhp_personnel_admin)
class DepartmentAdmin(
        ModelAdminMixin, admin.ModelAdmin):

    form = DepartmentForm

    fieldsets = (
        (None, {
            'fields': (
                'hod',
                'dept_name',
                'description',
            )}),
        audit_fieldset_tuple)

    search_fields = ['hod', 'dept_name', ]
