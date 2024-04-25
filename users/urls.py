from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (RegisterView, UserDeleteView, UserDetailView,
                         UserUpdateView, restore_access, verify)

app_name = UsersConfig.name

urlpatterns = [

    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="register"),
    path("verify/<str:token>", verify, name="verify"),
    path("restore_access/", restore_access, name="restore"),
    path("user_detail/", UserDetailView.as_view(), name="user_detail"),
    path("user_update/", UserUpdateView.as_view(), name="user_update"),
    path("user_delete/", UserDeleteView.as_view(), name="user_delete"),
    # path("user_list/", UserListView.as_view(), name="user_list"),
    path("", LoginView.as_view(template_name="users/login.html"), name="login")
]
