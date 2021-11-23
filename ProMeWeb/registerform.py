from django import forms
from ProMeAPI.models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'phone', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }