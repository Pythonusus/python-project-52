from django.contrib.auth.models import AbstractUser
from django.db import models

from task_manager.texts import user_model


class User(AbstractUser):
    # Overriding AbstractUser fields blank=True to blank=False
    first_name = models.CharField(
        verbose_name=user_model['first_name'],
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name=user_model['last_name'],
        max_length=150,
        blank=False,
        null=False,
    )
