from django import forms

mode_list = [
    ('pedestrian', 'Pedestrian'),
    ('fastest', 'Fastest'),
    ('bicycle', 'Bicycle'),
]

class StreetRouteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mode'].widget = forms.RadioSelect(choices=mode_list)
    source = forms.CharField(label='Source', max_length=255)
    destination = forms.CharField(label='Destination', max_length=255)
    mode = forms.CharField(label='Mode of Transport')