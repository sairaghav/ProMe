from django import forms
from ProMeAPI.models import StreetList

class StreetRiskForm(forms.ModelForm):
    class Meta:
        model = StreetList
        fields = '__all__'