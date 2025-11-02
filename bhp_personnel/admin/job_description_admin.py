from django.forms import Textarea
from django.db import models

from django.contrib import admin
from ..models import JobDescription, JobProfileKpa, FamiliarizationTime, SkillsKnowledge, JobDescriptionKpa
from ..admin_site import bhp_personnel_admin
from .modeladmin_mixins import ModelAdminMixin
from edc_model_admin.model_admin_audit_fields_mixin import (
    audit_fieldset_tuple)
from ..forms import JobDescriptionForm, JobDescriptionKpaForm, FamiliarizationTimeForm, SkillsKnowledgeForm
from edc_model_admin import StackedInlineMixin


class JobDescriptionKpaInline(StackedInlineMixin, admin.StackedInline):

    model = JobDescriptionKpa
    form = JobDescriptionKpaForm

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 500,
                   'cols': 70,
                   'style': 'height: 7em;'})},
    }

    extra = 1
    max_num = 20
    fieldsets = (
        (None, {
            'fields': [
                'key_performance_area',
                'kpa_tasks',
            ]}
         ),)


class SkillsKnowledgeTimeInline(StackedInlineMixin, admin.StackedInline):

    model = SkillsKnowledge
    form = SkillsKnowledgeForm
    extra = 0
    max_num = 3
    fieldsets = (
        (None, {
            'fields': [
                'skill',
                'attributes',
            ]}
         ),)


class FamiliarizationTimeInline(StackedInlineMixin, admin.StackedInline):

    model = FamiliarizationTime
    form = FamiliarizationTimeForm
    extra = 0
    max_num = 1
    fieldsets = (
        (None, {
            'fields': [
                'pre_appointment',
                'post_appointment',
            ]}
         ),)


@admin.register(JobDescription, site=bhp_personnel_admin)
class JobDescriptionAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = JobDescriptionForm

    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 500,
                   'cols': 70,
                   'style': 'height: 7em;'})},
    }

    inlines = [JobDescriptionKpaInline, SkillsKnowledgeTimeInline, FamiliarizationTimeInline]
    fieldsets = (
        (None, {
            'fields': (
                'job_title',
                'job_purpose',
                'qualifications',
                'department',
                'experience',
            )}),
        audit_fieldset_tuple)

    search_fields = ('job_title', 'department__dept_name', )

    def has_change_permission(self, request, obj=None):
        if 'HR' in request.user.groups.values_list('name', flat=True):
            return True
        return False

    def has_add_permission(self, request):
        if 'HR' in request.user.groups.values_list('name', flat=True):
            return True
        return False
