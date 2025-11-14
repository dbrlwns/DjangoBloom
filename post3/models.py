from django.db import models

# Create your models here.
class Content(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="작성자", null=False, blank=False, related_name="post3ContentUser")
    content = models.CharField("내용", max_length=100, blank=False, null=False)
    pub_date = models.DateTimeField("addedDate", auto_created=True, auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.content}"

class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="작성자", null=False, blank=False, related_name="post3CommentUser")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="답변들", null=False, blank=False)
    comment = models.CharField("content", max_length=100, blank=False, null=False)
    pub_date = models.DateTimeField("addedDate", auto_created=True, auto_now_add=True)

    def __str__(self):
        return f"Comment-{self.id}"