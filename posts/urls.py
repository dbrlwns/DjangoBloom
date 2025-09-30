from django.urls import path
from posts.views import show_posts, post_detail, post_add, post_delete

urlpatterns = [
    path('', show_posts, name="show_posts"),
    path('<int:postId>/', post_detail, name="post_detail"),
    path('add/', post_add, name="post_add"),
    path('<int:postId>/delete/', post_delete, name="post_delete"),


]