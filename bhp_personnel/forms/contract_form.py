from django import forms
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidator, FormValidatorMixin

from ..models import Contract, ContractExtension


class ContractFormValidator(FormValidator):

    def clean(self):
        super().clean()

        duration = self.cleaned_data.get('duration')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if duration == '2 Years':
            next_date = start_date + relativedelta(years=2)
            next_date -= timedelta(days=1)

            if next_date != end_date:
                message = {'duration':
                           'Contract duration must '
                           'match the contract start and end date'}
                self._errors.update(message)
                raise ValidationError(message)

        if duration == '1 Year':
            next_date = start_date + relativedelta(years=1)
            next_date -= timedelta(days=1)

            if next_date != end_date:
                message = {'duration':
                           'Contract duration must '
                           'match the contract start and end date'}
                self._errors.update(message)
                raise ValidationError(message)

        if duration == '6 Months':
            next_date = start_date + relativedelta(months=6)
            next_date -= timedelta(days=1)

            if next_date != end_date:
                message = {'duration':
                           'Contract duration must '
                           'match the contract start and end date'}
                self._errors.update(message)
                raise ValidationError(message)

        self.validate_active_contract()

    def validate_active_contract(self):

        identifier = self.cleaned_data.get('identifier')
        status = self.cleaned_data.get('status')

        if status == 'Active':
            active_contract = Contract.objects.filter(
                status='Active',
                identifier=identifier,).exclude(id=self.instance.id)
            if active_contract:
                message = {'status': "Two contracts can't be "
                                     "active at the same time"}
                self._errors.update(message)
                raise ValidationError(message)


class ContractForm(FormValidatorMixin, SiteModelFormMixin, forms.ModelForm):

    form_validator_cls = ContractFormValidator

    identifier = forms.CharField(
        label='Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        contract_extensions = int(
            self.data.get('contractextension_set-TOTAL_FORMS'))
        if contract_extensions > 1:
            message = {'identifier':
                       'Can not have more than 1 contract extension filled out'
                       '. Please remove the second instance.'}
            raise ValidationError(message)
        status = cleaned_data.get('status')
        if status == 'Not Active' and contract_extensions:
            message = {'This contract is not active.'}
            raise ValidationError(message)

    class Meta:
        model = Contract
        fields = '__all__'


class ContractExtensionForm(forms.ModelForm):

    class Meta:
        model = ContractExtension
        fields = '__all__'
