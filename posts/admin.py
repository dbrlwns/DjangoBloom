from django.contrib import admin
from posts.models import Post, PostImage, Comment
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail("image")
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "content",
        "created",
    ]

    inlines = [PostImageInline, ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(PostImage)
@admin_thumbnails.thumbnail("image")
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "image",
    ]


