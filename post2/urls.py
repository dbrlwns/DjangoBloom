from django.urls import path, include

from post2.views import default_view, create_post, new_detail, new_list, new_delete

urlpatterns = [
    path('', default_view),
    path('tinymce/', include('tinymce.urls')),
    path('newPost/', create_post, name="createPost"),
    path('newDetail/<int:postId>/', new_detail, name="postDetail"),
    path('newList/', new_list, name="showPostList"),
    path('newDelete/<int:postId>/', new_delete, name="postDelete"),
]