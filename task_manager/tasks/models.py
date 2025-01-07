from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        default=1,
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='authored_tasks',
    )

    executor = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
