from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from .employee import Employee


class Licence(BaseUuidModel):
    employee = models.ForeignKey(Employee,
                                 on_delete=models.CASCADE,
                                 )

    name = models.CharField(max_length=150, blank=True,
                            null=True,
                            verbose_name='License Name')

    number = models.CharField(max_length=50, blank=True,
                              null=True,
                              verbose_name='License Number')

    issued_by = models.CharField(max_length=100,
                                 verbose_name='Issued By')

    issue_date = models.DateField(verbose_name='Issue Date')

    expiration_date = models.DateField(verbose_name='Expiration Date')

    is_active = models.BooleanField(default=True,
                                    verbose_name='Is Active')

    notes = models.TextField(blank=True,
                             null=True,
                             verbose_name='Notes')

    class Meta:
        verbose_name_plural = 'Licenses'
