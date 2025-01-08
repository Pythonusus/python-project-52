from django.db import models

from task_manager.texts import status_model


class Status(models.Model):
    name = models.CharField(
        verbose_name=status_model['name'],
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        verbose_name=status_model['created_at'],
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
