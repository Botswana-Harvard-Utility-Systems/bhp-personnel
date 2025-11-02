from django.contrib import admin
from ..models import Contracting
from ..admin_site import bhp_personnel_admin
from .modeladmin_mixins import ModelAdminMixin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from ..forms import ContractingForm


@admin.register(Contracting, site=bhp_personnel_admin)
class ContractingAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = ContractingForm
    fieldsets = (
        (None, {
            'fields': (
                'contract',
                'identifier',
                'job_description',
                'skills',
            )}),
        audit_fieldset_tuple)

    filter_horizontal = ('skills',)
    list_filter = ('job_description',)
    search_fields = ('identifier', )
    autocomplete_fields = ['job_description', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

