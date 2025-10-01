from django import forms
from django.forms.models import ModelForm

from posts.models import Post, PostImage, Comment


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



