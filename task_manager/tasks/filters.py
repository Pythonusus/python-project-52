from django import forms
from django.contrib.auth import get_user_model
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter

from task_manager import texts
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        queryset=Status.objects.all(),
        label=texts.tasks_index['status']
    )
    executor = ModelChoiceFilter(
        queryset=User.objects.all(),
        label=texts.tasks_index['executor']
    )
    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=texts.tasks_index['label']
    )
    self_tasks = BooleanFilter(
        method='filter_self_tasks',
        widget=forms.CheckboxInput,
        label=texts.tasks_index['self_tasks']
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
