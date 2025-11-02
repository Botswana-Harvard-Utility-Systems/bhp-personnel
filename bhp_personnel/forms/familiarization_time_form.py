from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import FamiliarizationTime


class FamiliarizationTimeForm(SiteModelFormMixin, forms.ModelForm):
    class Meta:
        model = FamiliarizationTime
        fields = '__all__'
