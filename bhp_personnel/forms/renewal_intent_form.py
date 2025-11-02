from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import RenewalIntent, Contract


class RenewalIntentForm(SiteModelFormMixin, forms.ModelForm):
    contract = forms.ModelChoiceField(
        label='Contract',
        queryset=Contract.objects.none(),
    )

    def __init__(self, *args, **kwargs):
        contract = self.request.GET.get('contract')
        super().__init__(*args, **kwargs)
        if contract:
            self.fields['contract'].queryset = Contract.objects.filter(id=contract)

    class Meta:
        model = RenewalIntent
        fields = '__all__'
