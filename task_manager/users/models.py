from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Overriding AbstractUser fields blank=True to blank=False
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
