from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import JobProfileKpa


class JobProfileKpaForm(SiteModelFormMixin, forms.ModelForm):
    class Meta:
        model = JobProfileKpa
        fields = '__all__'
