from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .contract import Contract
from .job_description import JobDescription
from .list_models import Skills


class Contracting(BaseUuidModel, SiteModelMixin, models.Model):

    identifier = models.CharField(
        verbose_name='Employee Identifier',
        max_length=36,
        blank=True)

    contract = models.OneToOneField(
        Contract,
        on_delete=models.PROTECT,
        default=0,
        blank=True,
        null=True,
        related_name='contracting'
        )

    job_description = models.ForeignKey(
        JobDescription, on_delete=models.PROTECT,
        null=True,)

    skills = models.ManyToManyField(
        Skills,
        verbose_name='Which professional skills does this personnel have? ',
        max_length=40, )

    def __str__(self):
        return self.job_description

    class Meta:
        app_label = 'bhp_personnel'
        unique_together = ('identifier', 'contract')
        verbose_name = 'Contracting'
        verbose_name_plural = 'Contracting'
