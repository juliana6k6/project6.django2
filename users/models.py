import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", **NULLABLE)
    phone_number = models.CharField(
        max_length=35, verbose_name="номер телефона", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="страна", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatar/", verbose_name="Аватар", **NULLABLE
    )
    token = models.CharField(max_length=50, verbose_name="токен")
    # verify_code = models.UUIDField(
    #     default=uuid.uuid4, verbose_name="Код вeрификации", editable=False
    # )
    is_blocked = models.BooleanField(
        verbose_name="блокировка пользователя", default=False
    )
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ('block_users', 'Заблокuровать пользователя')]



