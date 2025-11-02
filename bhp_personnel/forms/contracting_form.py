from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import Contracting, Contract


class ContractingForm(SiteModelFormMixin, forms.ModelForm):
    contract = forms.ModelChoiceField(
        label='Contract',
        queryset=Contract.objects.none(),
    )

    def __init__(self, *args, **kwargs):
        contract = self.request.GET.get('contract')
        super().__init__(*args, **kwargs)
        self.fields['identifier'].widget.attrs['readonly'] = True
        if contract:
            self.fields['contract'].queryset = Contract.objects.filter(id=contract)

    class Meta:
        model = Contracting
        fields = '__all__'
