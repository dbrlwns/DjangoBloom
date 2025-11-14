from django import forms
from django.forms import ModelForm

from post3.models import Content, Comment


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["content"]

