from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .job_description import JobDescription


class JobProfileKpa(BaseUuidModel, SiteModelMixin, models.Model):

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.PROTECT)

    key_performance_area = models.CharField(
        verbose_name='KEY PERFORMANCE AREAS',
        max_length=100,
        blank=True,
        null=True)

    kpa_tasks = models.TextField(
        verbose_name='TASKS',
        max_length=None)

    class Meta:
        verbose_name = 'Job Description KPA'
        verbose_name_plural = 'Job Description KPA'
