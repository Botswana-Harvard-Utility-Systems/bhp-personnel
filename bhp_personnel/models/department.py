from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin


class DepartmentManager(models.Manager):
    def get_by_natural_key(self, hod, dept_name):
        return self.get(hod=hod, dept_name=dept_name)


class Department(BaseUuidModel, SiteModelMixin, models.Model):

    hod = models.CharField(
        verbose_name="Head Of Department",
        max_length=50,
        null=False,
    )

    dept_name = models.CharField(
        verbose_name="Department Name",
        max_length=50,
        null=False,
    )

    description = models.TextField(
        verbose_name='Description',
        max_length=500,
        blank=True
    )

    objects = DepartmentManager()

    def natural_key(self):
        return (self.hod, self.dept_name)

    def __str__(self):
        return f'{self.dept_name}'

    class Meta:
        app_label = 'bhp_personnel'
        verbose_name = 'Department'
        verbose_name_plural = 'Department'
