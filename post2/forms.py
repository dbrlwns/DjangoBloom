from django import forms
from .models import Blog2

class BlogPost(forms.ModelForm):
    class Meta:
        model = Blog2
        fields=['title', 'description']