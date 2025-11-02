from django import forms

from edc_base.sites import SiteModelFormMixin
from ..models import PerformanceReview


class PerformanceReviewForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = PerformanceReview
        fields = '__all__'
