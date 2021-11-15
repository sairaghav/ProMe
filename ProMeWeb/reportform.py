from django import forms
from ProMeAPI.models import StreetRisk

class StreetReportForm(forms.ModelForm):
    class Meta:
        model = StreetRisk
        fields = ['street', 'news','tags']