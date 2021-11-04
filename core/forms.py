from typing import Hashable
from django import forms
from django_quill.forms import QuillFormField

from core.models import Article, User

class RegisterForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=64, required=True)
    class Meta:
        model = User
        fields=["Name", "Email"]

class LogInUserForm(forms.Form):
    NameOrEmail = forms.CharField(max_length=50, label="Name or Email", required=True)
    Password = forms.CharField(widget=forms.PasswordInput, max_length=64, required=True)

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["Title", "Body"]