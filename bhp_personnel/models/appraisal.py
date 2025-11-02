from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin

from .contract import Contract
from ..choices import ASSESSMENT_TYPE


class Appraisal(BaseUuidModel, SiteModelMixin, models.Model):
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

    assessment_type = models.CharField(
        verbose_name='Review-Type',
        max_length=50,
        choices=ASSESSMENT_TYPE)

    supervisor_signature = models.CharField(
        verbose_name='Supervisor Signature',
        max_length=25,
        help_text='Write your full name to confirm that you have approved this appraisal.',
        blank=True,
        null=True
    )

    date_supervisor_signed = models.DateField(
        verbose_name="Date Supervisor Signed",
        blank=True,
        null=True
    )

    employee_signature = models.CharField(
        verbose_name='Employee Signature',
        max_length=25,
        help_text='Write your full name to confirm that you have approved this appraisal.',
        blank=True,
        null=True
    )

    date_employee_signed = models.DateField(
        verbose_name="Date Employee Signed",
        blank=True,
        null=True
    )

    additional_comments = models.TextField(
        verbose_name='Additional Comments For example, staff member’s job changed'
                     ' in the middle of the review period, '
                     'employee on leave of absence, staff member works for '
                     'more than one supervisor, etc',
        max_length=1000,
        blank=True,
        null=True)

    staff_comments = models.TextField(
        verbose_name='Employee comment',
        max_length=1000,
        blank=True,
        null=True)

    def __str__(self):
        return f'{self.emp_identifier} - {self.assessment_type}'

    class Meta:
        app_label = 'bhp_personnel'
        verbose_name = 'Appraisal'
        verbose_name_plural = 'Appraisal'
        unique_together = ('emp_identifier', 'contract', 'assessment_type')
