from django.db import models


class Status(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
