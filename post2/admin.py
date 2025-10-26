from django.contrib import admin

from post2.models import Blog2


# Register your models here.
@admin.register(Blog2)
class Post2Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]