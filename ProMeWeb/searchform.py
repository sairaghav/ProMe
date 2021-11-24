from django import forms
from ProMeAPI.models import StreetList

class StreetRiskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['news_from'].required = False
        self.fields['news_till'].required = False

    class Meta:
        model = StreetList
        fields = ['street', 'news_from', 'news_till']
        widgets = {
            'news_from': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
            'news_till': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'})
        }