from django import forms

from .models import CHAR_FIELD_LENGHT


# define Registration Form to validate it in views
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=CHAR_FIELD_LENGHT)
    name = forms.CharField(max_length=CHAR_FIELD_LENGHT)
    surname = forms.CharField(max_length=CHAR_FIELD_LENGHT)
    password = forms.CharField(max_length=CHAR_FIELD_LENGHT)
    email = forms.EmailField()
