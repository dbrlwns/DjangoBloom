from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="작성자")

    title = models.CharField("title")
    content = models.TextField("content")
    created = models.DateTimeField("작성일시", auto_now_add=True)

    objects = models.Manager() # explicit declaration, Unresolved attr Warning 방지


class PostImage(models.Model):
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, verbose_name="포스트")
    image = models.ImageField(verbose_name="이미지", upload_to="post",
                              validators=[FileExtensionValidator(allowed_extensions=['png','jpg','jpeg','gif'])])




























