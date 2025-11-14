from django.urls import path

from post3.views import post3_page

app_name = "post3"
urlpatterns = [
    path('', post3_page),
]