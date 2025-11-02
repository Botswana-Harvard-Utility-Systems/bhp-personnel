from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .job_description import JobDescription


class FamiliarizationTime(BaseUuidModel, SiteModelMixin, models.Model):

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.PROTECT)

    pre_appointment = models.TextField(
        verbose_name='Pre Appointment',
        max_length=200)

    post_appointment = models.TextField(
        verbose_name='Post Appointment',
        max_length=200)

    class Meta:
        verbose_name = 'Familiarization Time'
        verbose_name_plural = 'Familiarization Time'
