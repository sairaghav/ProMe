from django import forms
from ProMeAPI.models import StreetRisk

class StreetRiskForm(forms.ModelForm):
    class Meta:
        model = StreetRisk
        fields = ['street_name']