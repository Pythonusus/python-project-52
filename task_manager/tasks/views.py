from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager import texts
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TasksIndexView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'tasks_index': texts.tasks_index,
    }


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Create a new task.
    Redirects to the tasks index page after successful creation.
    Shows a success message after successful creation.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = texts.create_task['create_success']
    extra_context = {
        'base': texts.base,
        'create_task': texts.create_task,
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """
    Update a task.
    Redirects to the tasks index page after successful update.
    Shows a success message after successful update.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_index')
    success_message = texts.update_task['update_success']
    extra_context = {
        'base': texts.base,
        'update_task': texts.update_task,
    }


class TaskDeleteView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     PermissionRequiredMixin,
                     DeleteView):
    """
    Delete a task. Tasks can only be deleted by the author.
    Redirects to the tasks index page after successful deletion.
    Shows a success message after successful deletion.
    """
    model = Task
    template_name = 'tasks/delete.html'
    permission_required = 'tasks.delete_task'

    success_url = reverse_lazy('tasks_index')
    success_message = texts.delete_task['delete_success']

    extra_context = {
        'base': texts.base,
        'delete_task': texts.delete_task,
    }

    def has_permission(self):
        """
        Overriding has_permission method from PermissionRequiredMixin.
        Allows deleting tasks only by the author.
        """
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """
        Overriding handle_no_permission method from AccessMixin.
        Handles the case when the user is not authenticated or doesn't have
        permission to delete the task.
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, texts.auth['auth_required'])
            return redirect(reverse_lazy('login'))

        messages.error(self.request, texts.auth['permission_required'])
        return redirect(reverse_lazy('tasks_index'))
