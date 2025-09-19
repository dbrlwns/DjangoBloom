from django.urls import path

from users.views import user_login, user_index, user_logout, user_signup, user_info, user_edit

urlpatterns = [
    path('', user_index, name='user_index'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('signup/', user_signup, name='user_signup'),
    path('userinfo/', user_info, name='user_info'),
    path('userEdit/', user_edit, name='user_edit'),
]