from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager import texts
from task_manager.mixins import OwnershipRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TasksIndexView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
    filterset_class = TaskFilter
    extra_context = {
        'base': texts.base,
        'tasks_index': texts.tasks_index,
    }


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Create a new task. Sets author to the current user.
    Redirects to the tasks index page after successful creation.
    Shows a success message after successful creation.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_index')
    success_message = texts.create_task['create_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'create_task': texts.create_task,
    }

    def form_valid(self, form):
        """
        Set the author of the task to the current user.
        """
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
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'update_task': texts.update_task,
    }


class TaskDeleteView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     OwnershipRequiredMixin,
                     DeleteView):
    """
    Delete a task. Tasks can only be deleted by the author.
    Redirects to the tasks index page after successful deletion.
    Shows a success message after successful deletion.
    """
    model = Task
    template_name = 'tasks/delete.html'
    permission_required = 'tasks.delete_task'

    # OwnershipRequiredMixin settings
    ownership_field = 'author'
    permission_denied_redirect_url = 'tasks_index'
    permission_denied_message = texts.delete_task['delete_error']
    success_url = reverse_lazy('tasks_index')
    success_message = texts.delete_task['delete_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'delete_task': texts.delete_task,
    }


class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'task_view': texts.task_view,
    }
