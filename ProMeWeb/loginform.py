from django import forms
from ProMeAPI.models import User

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }