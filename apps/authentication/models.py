from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


class CustomUser(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    username = models.CharField(
        max_length=200,
    )

    email = models.EmailField(
        unique=True,
        max_length=200,
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:

        verbose_name = "CustomUser"

        verbose_name_plural = "CustomUsers"

        ordering = ["-id"]

    def __str__(self): # pragma: no cover
        return f"{self.username}"
