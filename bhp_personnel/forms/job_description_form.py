from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import JobDescription


class JobDescriptionForm(SiteModelFormMixin, forms.ModelForm):

    # identifier = forms.CharField(
    #     label='Identifier',
    #     widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    # job_title = forms.CharField(
    #     label='Job Title',
    #     widget=forms.TextInput(attrs={'readonly': 'readonly', 'size': 40}))

    class Meta:
        model = JobDescription
        fields = '__all__'
