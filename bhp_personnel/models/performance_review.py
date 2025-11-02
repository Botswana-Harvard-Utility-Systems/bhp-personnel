from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .appraisal import Appraisal


class PerformanceReview(BaseUuidModel, SiteModelMixin, models.Model):

    appraisal = models.ForeignKey(
        Appraisal,
        on_delete=models.PROTECT)

    kpa_title = models.CharField(
        verbose_name='Key performance areas',
        max_length=100,
        blank=True,
        null=True)

    kpa_description = models.TextField(
        verbose_name='Key performance area description',
        max_length=400,
        blank=True,
        null=True
    )

    review_score = models.PositiveIntegerField(
        verbose_name='Review Score',
        blank=True,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        null=True)

    class Meta:
        verbose_name = 'Perfomance Review'

    def __str__(self):
        return f'{self.kpa_title}'
