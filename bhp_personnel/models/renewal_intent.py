from django.db import models

from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from django.core.validators import FileExtensionValidator
from edc_constants.choices import YES_NO

from .contract import Contract


class RenewalIntent(BaseUuidModel, SiteModelMixin):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE
    )

    intent = models.CharField(
        verbose_name="Do you intend on renewing contract",
        max_length=10,
        choices=YES_NO,
        help_text='Yes or NO'
    )

    letter_upload = models.FileField(upload_to='intent_letter/',
                                     validators=[FileExtensionValidator(['pdf']), ],
                                     verbose_name="Upload letter of intent"
                                     )

    comment = models.TextField(
        verbose_name="Supervisor comment",
        blank=True,
        null=True
    )

    date_submitted = models.DateTimeField(
        verbose_name="Date created",
        auto_now=True
    )

    def __str__(self):
        return f'{self.contract} - {self.intent}'

    class Meta:
        app_label = 'bhp_personnel'
        verbose_name = 'Intent To Renew'
        verbose_name_plural = 'Intent To Renew'
