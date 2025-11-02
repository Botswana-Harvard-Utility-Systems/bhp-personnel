from django.db import models
from django.forms import Textarea

from django.contrib import admin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)

from ..admin_site import bhp_personnel_admin
from .modeladmin_mixins import ModelAdminMixin
from ..forms import RenewalIntentForm
from ..models import RenewalIntent


@admin.register(RenewalIntent, site=bhp_personnel_admin)
class RenewalIntentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = RenewalIntentForm

    fieldsets = (
        (None, {
            'fields': (
                'contract',
                'intent',
                'letter_upload',
                'comment'

            )}),
        audit_fieldset_tuple)
    radio_fields = {
        "intent": admin.VERTICAL,
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form




