from django import forms
from django.contrib.auth import get_user_model

from edc_base.sites import SiteModelFormMixin

from ..models import Employee, Supervisor, JobDescription

User = get_user_model()


class EmployeeForm(SiteModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['identifier'].required = False

    identifier = forms.CharField(
        label='Employee Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    job_title = forms.ModelChoiceField(
        label='Job Title',
        queryset=JobDescription.objects.all(),
        to_field_name='job_title',
        widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if self.instance._state.adding or ('email' in self.cleaned_data):
            self.validate_unique_email(email)
        return cleaned_data

    def validate_unique_email(self, email: str):
        if not email:
            return
        qs = self._meta.model.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                {'email': 'An employee with this email already exists.'})

    class Meta:
        model = Employee
        fields = '__all__'


class SupervisorForm(forms.ModelForm):

    class Meta:
        model = Supervisor
        fields = '__all__'
