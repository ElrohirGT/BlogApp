from typing import Hashable
from django import forms

class CreateUserForm(forms.Form):
    Name =  forms.CharField(max_length=50, label="User Name", required=True)
    Email = forms.EmailField(max_length=50, required=True)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=64, required=True)

class LogInUserForm(forms.Form):
    NameOrEmail = forms.CharField(max_length=50, label="Name or Email", required=True)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=64, required=True)