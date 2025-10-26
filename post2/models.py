from django.db import models
# from ckeditor_uploader.fields import RichTextUploadingField
from tinymce.models import HTMLField

# Create your models here.

class Blog2(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="작성자", null=True, blank=True)
    title = models.CharField(max_length=100)
    description = HTMLField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title
