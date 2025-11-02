from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .contracting import Contracting


class JobPerformanceKpa(BaseUuidModel, SiteModelMixin, models.Model):

    contracting = models.ForeignKey(
        Contracting,
        on_delete=models.PROTECT)

    key_performance_area = models.CharField(
        verbose_name='KEY PERFORMANCE AREAS',
        max_length=100)

    kpa_tasks = models.TextField(
        verbose_name='TASKS',
        max_length=1000)

    kpa_performance_indicators = models.TextField(
        verbose_name='PERFORMANCE INDICATORS'
                     '(completion dates)',
        max_length=1000)

    skills_required = models.TextField(
        verbose_name="SKILLS REQUIRED",
        max_length=100)

    class Meta:
        verbose_name = 'Job Performance KPA'
        verbose_name_plural = 'Job Performance KPA'
