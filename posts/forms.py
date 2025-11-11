from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.forms.models import ModelForm

from posts.models import Post, PostImage, Comment


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

    def clean_title(self):

        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise ValidationError("제목을 입력해주세요")
        return title
    def clean_content(self):
        content = self.cleaned_data.get("content", "").strip()
        if not content:
            raise ValidationError("내용을 입력해주세요")
        return content

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']
PostImageFormSet = inlineformset_factory(
    Post,
    PostImage,
    fields=('image', ),
    extra=1,
    can_delete=True
)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



