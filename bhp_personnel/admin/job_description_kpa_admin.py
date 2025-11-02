from django.contrib import admin
from ..models import JobDescriptionKpa
from ..admin_site import bhp_personnel_admin
from .modeladmin_mixins import ModelAdminMixin

from ..forms import JobDescriptionKpaForm


@admin.register(JobDescriptionKpa, site=bhp_personnel_admin)
class JobDescriptionKpaAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = JobDescriptionKpaForm

    fieldsets = (
        (None, {
            'fields': [
                'key_performance_area',
                'kpa_tasks',
                'kpa_performance_indicators',
                'skills_required', ]}
         ),)
