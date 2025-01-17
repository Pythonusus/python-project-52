from django.contrib.auth import get_user_model
from django.db import models

from task_manager.statuses.models import Status
from task_manager.texts import task_model


class Task(models.Model):
    name = models.CharField(
        verbose_name=task_model['name'],
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    description = models.TextField(
        verbose_name=task_model['description'],
        max_length=1000,
        blank=True,
        null=True,
    )

    # Atleast one status must be created before creating a task
    # Does not allow deleting statuses that are in use
    status = models.ForeignKey(
        Status,
        verbose_name=task_model['status'],
        on_delete=models.PROTECT,
        related_name='tasks',
    )

    # Author is set automatically by the view as the current user
    # Does not allow deleting users that are authors of tasks
    author = models.ForeignKey(
        get_user_model(),
        verbose_name=task_model['author'],
        on_delete=models.PROTECT,
        related_name='authored_tasks',
    )

    # Does not allow deleting users that are executors of tasks
    executor = models.ForeignKey(
        get_user_model(),
        verbose_name=task_model['executor'],
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=task_model['created_at'],
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
