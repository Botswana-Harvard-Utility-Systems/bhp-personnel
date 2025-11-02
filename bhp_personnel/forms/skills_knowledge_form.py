from django import forms
from edc_base.sites import SiteModelFormMixin
from ..models import SkillsKnowledge


class SkillsKnowledgeForm(SiteModelFormMixin, forms.ModelForm):
    class Meta:
        model = SkillsKnowledge
        fields = '__all__'
