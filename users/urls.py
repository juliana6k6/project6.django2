from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (RegisterView, UserDeleteView, UserDetailView,
                         UserUpdateView, restore_access, verify)

app_name = UsersConfig.name

urlpatterns = [
    path("", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegisterView.as_view(), name="register"),
    path("verify/<str:token>", verify, name="verify"),
    path("restore_access/", restore_access, name="restore"),
    path("user_detail/", UserDetailView.as_view(), name="user_detail"),
    path("userupdate/", UserUpdateView.as_view(), name="user_update"),
    path("userdelete/", UserDeleteView.as_view(), name="user_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
