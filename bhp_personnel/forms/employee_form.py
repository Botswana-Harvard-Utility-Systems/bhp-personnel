from django import forms
from django.contrib.auth import get_user_model

from edc_base.sites import SiteModelFormMixin

from ..models import Employee, Supervisor

User = get_user_model()


class EmployeeForm(SiteModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['identifier'].required = False

    identifier = forms.CharField(
        label='Employee Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        self.validate_unique_email(email)
        return cleaned

    def validate_unique_email(self, email: str):
        if not email:
            return
        exists = User.objects.filter(email__iexact=email).exists()
        if exists:
            raise forms.ValidationError(
                {'email': 'An account with this email already exists.'})

    class Meta:
        model = Employee
        fields = '__all__'


class SupervisorForm(forms.ModelForm):

    class Meta:
        model = Supervisor
        fields = '__all__'
