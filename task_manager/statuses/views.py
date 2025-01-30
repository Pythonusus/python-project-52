from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager import texts
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusesIndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'statuses_index': texts.statuses_index,
    }


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Create a new status.
    Redirects to the statuses index page after successful creation.
    Shows a success message after successful creation.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_index')
    success_message = texts.create_status['create_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'create_status': texts.create_status,
    }


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """
    Update a status.
    Redirects to the statuses index page after successful update.
    Shows a success message after successful update.
    """
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_index')
    success_message = texts.update_status['update_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'update_status': texts.update_status,
    }


class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses_index')
    success_message = texts.delete_status['delete_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'delete_status': texts.delete_status,
    }

    def post(self, request, *args, **kwargs):
        """
        Override the post method to check if the status is used in any tasks
        before deleting it.
        If status is in use, show an error message and redirect
        to the statuses index page.
        """
        in_use = self.get_object().tasks.exists()
        if in_use:
            messages.error(
                request,
                texts.delete_status['delete_error']
            )
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
