from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

import task_manager.texts as texts
from task_manager.users.forms import UserForm, UserUpdateForm
from django.contrib.auth import get_user_model


class UsersIndexView(ListView):
    model = get_user_model()
    template_name = 'users/index.html'
    context_object_name = 'users'
    extra_context = {
        'base': texts.base,
        'users_index': texts.users_index,
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    """
    Create a new user.
    Redirects to the login page after successful creation.
    Shows a success message after successful creation.
    """
    model = get_user_model()
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = texts.create_user['register_success']
    extra_context = {
        'base': texts.base,
        'create_user': texts.create_user,
    }


class UserUpdateView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     PermissionRequiredMixin,
                     UpdateView):
    """
    Update a user.
    Redirects to the users index page after successful update.
    Shows a success message after successful update.
    """
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    permission_required = 'auth.change_user'

    success_url = reverse_lazy('users_index')
    success_message = texts.update_user['update_success']

    extra_context = {
        'base': texts.base,
        'update_user': texts.update_user,
    }

    def has_permission(self):
        """
        Overriding has_permission method from PermissionRequiredMixin.
        Allows updating only the current user.
        """
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        """
        Overriding handle_no_permission method from AccessMixin.
        Handles the case when the user is not authenticated or doesn't have
        permission to update the user.
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, texts.auth['auth_required'])
            return redirect(reverse_lazy('login'))

        messages.error(self.request, texts.auth['permission_required'])
        return redirect(reverse_lazy('users_index'))


class UserDeleteView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     PermissionRequiredMixin,
                     DeleteView):
    """
    Delete a user.
    Redirects to the users index page after successful deletion.
    Shows a success message after successful deletion.
    """
    model = get_user_model()
    template_name = 'users/delete.html'
    permission_required = 'auth.delete_user'

    success_url = reverse_lazy('users_index')
    success_message = texts.delete_user['delete_success']

    extra_context = {
        'base': texts.base,
        'delete_user': texts.delete_user,
    }

    def has_permission(self):
        """
        Overriding has_permission method from PermissionRequiredMixin.
        Allows deleting only the current user.
        """
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        """
        Overriding handle_no_permission method from AccessMixin.
        Handles the case when the user is not authenticated or doesn't have
        permission to delete the user.
        """
        if not self.request.user.is_authenticated:
            messages.error(self.request, texts.auth['auth_required'])
            return redirect(reverse_lazy('login'))

        messages.error(self.request, texts.auth['permission_required'])
        return redirect(reverse_lazy('users_index'))
