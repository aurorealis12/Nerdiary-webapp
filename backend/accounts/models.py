from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Replaces the `uzytkownik` table. Django handles password hashing."""

    email = models.EmailField(unique=True)
    country = models.CharField(max_length=255, blank=True)
