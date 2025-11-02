from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from edc_base.sites import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel

from .performance_assessment import Contract
from ..choices import PERFORMANCE_RATING, ASSESSMENT_TYPE


class KeyPerformanceArea(SiteModelMixin, BaseUuidModel):
    emp_identifier = models.CharField(
        verbose_name="Employee Identifier",
        max_length=36,
        null=True,
        blank=True)

    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    kpa_nd_objective = models.CharField(
        verbose_name='KEY PERFORMANCE AREA and OBJECTIVES',
        max_length=250, )

    performance_indicators = models.CharField(
        verbose_name='Key PERFORMANCE INDICATORS / MEASURES & DEADLINES '
                     '(completion dates)',
        max_length=150, )

    weighting = models.PositiveIntegerField(
        verbose_name='%WEIGHTING (KPA Weighting as % of total)',
        validators=[MaxValueValidator(100)],
        default=0,
        help_text="0 to 100"
    )

    kpa_rating = models.CharField(
        verbose_name='KPA RATING (Use Rating Scale)',
        max_length=2,
        choices=PERFORMANCE_RATING,
        help_text='<h4> NR - Not Rated,  </br>1 - Unacceptable Performance '
                  '</br>2 - Weak and Inconsistent Performance </br>3 - '
                  'Competent Meets Standards </br>4 - Exceeds Expectations '
                  '</br>5 - Exceptional Performance </h4>')

    kpa_score = models.CharField(
        verbose_name='KPA SCORE (Rating x Weighting)',
        max_length=50,
        blank=True)

    assessment_period_type = models.CharField(
        verbose_name='Period of ASSESSMENT (on Performance'
                     ' Results achieved)',
        max_length=15,
        choices=ASSESSMENT_TYPE)

    def save(self, *args, **kwargs):
        if self.weighting and self.kpa_rating:
            self.kpa_score = (self.weighting / 100) * int(self.kpa_rating)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Key Performance Areas'
        verbose_name_plural = 'Key Performance Areas'
        unique_together = ('emp_identifier', 'contract',
                           'kpa_nd_objective', 'assessment_period_type')
