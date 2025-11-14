from django.contrib import admin

from post3.models import Content, Comment


# Register your models here.
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass