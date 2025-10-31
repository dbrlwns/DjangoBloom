from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Blog2(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="작성자", null=True, blank=True)
    title = models.CharField(max_length=100)
    description = HTMLField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    # Append HashTag
    hashTag = models.ManyToManyField('post2.HashTag', blank=True)

    def __str__(self):
        return self.title

    objects = models.Manager()


class HashTag(models.Model):
    hash = models.CharField(max_length=10)

    def __str__(self):
        return self.hash

    objects = models.Manager()
