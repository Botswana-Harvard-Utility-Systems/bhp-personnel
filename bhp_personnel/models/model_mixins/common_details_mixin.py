from django.db import models
from edc_constants.choices import GENDER
from edc_base.model_validators import CellNumber
from django_crypto_fields.fields import EncryptedCharField


class CommonDetailsMixin(models.Model):

    first_name = models.CharField(
        verbose_name="First name",
        max_length=100)

    middle_name = models.CharField(
        verbose_name="Middle names",
        max_length=150,
        blank=True,
        null=True)

    last_name = models.CharField(
        verbose_name="Last name",
        max_length=100)

    gender = models.CharField(
        verbose_name='Gender',
        choices=GENDER,
        null=True,
        max_length=1)

    email = models.EmailField()

    hired_date = models.DateField(
        verbose_name='Hired Date')

    cell = EncryptedCharField(
        verbose_name='Contact Number',
        validators=[CellNumber, ],
        blank=False,
        unique=True)

    class Meta:
        abstract = True
