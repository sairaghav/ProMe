from django import forms
from ProMeAPI.models import StreetRisk
from ProMeAPI.services.config import trackingTags

tag_list = []

for tag in trackingTags:
    tag_list.append((tag.lower(),tag.capitalize()))

class StreetReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tags'].widget = forms.RadioSelect(choices=tag_list)
    class Meta:
        model = StreetRisk
        fields = ['street', 'news', 'tags']