from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from .department import Department


class JobDescription(BaseUuidModel, SiteModelMixin, models.Model):

    job_title = models.CharField(
        verbose_name='Job Title',
        max_length=100)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name='Business Unit')

    job_purpose = models.TextField(
        verbose_name='Job Purpose',
        max_length=2000)

    qualifications = models.CharField(
        verbose_name='Required Qualifications',
        max_length=500)

    experience = models.TextField(
        verbose_name='Required Experience',
        max_length=None)

    def __str__(self):
        return f'{self.job_title}'

    class Meta:
        app_label = 'bhp_personnel'
        verbose_name = 'Job Description'
        verbose_name_plural = 'Job Description'
