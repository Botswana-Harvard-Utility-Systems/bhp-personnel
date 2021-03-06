from django.db import models

from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_search.model_mixins import SearchSlugModelMixin as Base
from edc_base.model_mixins import BaseUuidModel

from ..identifier import PiIdentifier
from .employee import Employee
from .list_models import Studies
from .model_mixins import CommonDetailsMixin


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('first_name')
        fields.append('last_name')
        fields.append('email')
        fields.append('identifier')
        return fields

    class Meta:
        abstract = True


class Pi(CommonDetailsMixin, SiteModelMixin, BaseUuidModel):

    identifier_cls = PiIdentifier

    identifier = models.CharField(
        verbose_name="PI Identifier",
        max_length=36,
        null=True,
        blank=True,
        unique=True)

    studies = models.ManyToManyField(
        Studies,
        verbose_name='Which studies does this personnel belong to? ',
        max_length=20,
        blank=True,
        help_text='',
    )

    supervisor = models.ForeignKey(
        Employee,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name}, {self.last_name} {self.identifier}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)
