from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager import texts
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


class LabelsIndexView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'labels_index': texts.labels_index,
    }


class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Create a new label.
    Redirects to the labels index page after successful creation.
    Shows a success message after successful creation.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels_index')
    success_message = texts.create_label['create_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'create_label': texts.create_label,
    }


class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """
    Update a label.
    Redirects to the labels index page after successful update.
    Shows a success message after successful update.
    """
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_index')
    success_message = texts.update_label['update_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'update_label': texts.update_label,
    }


class LabelDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_index')
    success_message = texts.delete_label['delete_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'delete_label': texts.delete_label,
    }

    def post(self, request, *args, **kwargs):
        """
        Override the post method to check if the label is used in any tasks
        before deleting it.
        If label is in use, show an error message and redirect
        to the labels index page.
        """
        in_use = self.get_object().tasks.exists()
        if in_use:
            messages.error(
                request,
                texts.delete_label['delete_error']
            )
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
