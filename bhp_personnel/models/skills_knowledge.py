from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .job_description import JobDescription


class SkillsKnowledge(BaseUuidModel, SiteModelMixin, models.Model):

    job_description = models.ForeignKey(
        JobDescription,
        on_delete=models.PROTECT)

    skill = models.CharField(
        verbose_name='Skill & Knowledge',
        max_length=100)

    attributes = models.TextField(
        verbose_name='Attributes',
        max_length=1000)
    class Meta:
        verbose_name = 'Skills & Knowledge'
        verbose_name_plural = 'Skills & Knowledge'
