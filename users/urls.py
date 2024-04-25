from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (RegisterView, UserDetailView,
                         UserProfileView, restore_access, verify, UserListView, blocked_users)

app_name = UsersConfig.name

urlpatterns = [

    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="register"),
    path("verify/<str:token>", verify, name="verify"),
    path("restore_access/", restore_access, name="restore"),
    path("user_detail/", UserDetailView.as_view(), name="user_detail"),
    path("user_update/", UserProfileView.as_view(), name="user_profile"),
    path("user_list/", UserListView.as_view(), name="user_list"),
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path('user_activity/<int:pk>/', blocked_users, name='users_block'),
]
