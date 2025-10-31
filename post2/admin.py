from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.forms.widgets import CheckboxSelectMultiple

from post2.models import Blog2, HashTag


# Register your models here.
@admin.register(Blog2)
class Post2Admin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]

    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass