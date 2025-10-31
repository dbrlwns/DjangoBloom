from django.urls import path, include

from post2.views import default_view, create_post, new_detail, new_list, new_delete, api_new, new_tag, postEdit

app_name = "post2"
urlpatterns = [
    path('', default_view),
    path('tinymce/', include('tinymce.urls')),
    path('newPost/', create_post, name="createPost"),
    path('newDetail/<int:postId>/', new_detail, name="postDetail"),
    path('newList/', new_list, name="showPostList"),
    path('newDelete/<int:postId>/', new_delete, name="postDelete"),
    path('new-api/', api_new, name="apiTest"),
    path('newList/tag/<str:tag_name>/', new_tag, name="tags"),
    path('<int:postId>/edit/', postEdit, name="editPost"),
]