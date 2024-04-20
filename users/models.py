import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None
    first_lastname = models.CharField(max_length=100, verbose_name="ФИО", **NULLABLE)
    phone_number = models.CharField(
        max_length=35, verbose_name="номер телефона", **NULLABLE)
    country = models.CharField(max_length=50, verbose_name="страна", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatar/", verbose_name="Аватар", **NULLABLE
    )
    token = models.CharField(max_length=50, verbose_name="токен")
    verify_code = models.UUIDField(
        default=uuid.uuid4, verbose_name="Код вeрификации", editable=False
    )
    is_bloked = models.BooleanField(
        verbose_name="блокировка пользователя", default=False
    )
    comment = models.TextField(verbose_name="комментарий", **NULLABLE)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
