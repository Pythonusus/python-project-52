from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

import task_manager.texts as texts
from task_manager.users.forms import UserForm, UserUpdateForm
from task_manager.users.models import User


class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    extra_context = {
        'base': texts.base,
        'users_index': texts.users_index,
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
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
    model = User
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
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, texts.auth['auth_required'])
            return redirect(reverse_lazy('login'))

        messages.error(self.request, texts.auth['permission_required'])
        return redirect(reverse_lazy('users_index'))


class UserDeleteView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     PermissionRequiredMixin,
                     DeleteView):
    model = User
    template_name = 'users/delete.html'
    permission_required = 'auth.delete_user'

    success_url = reverse_lazy('users_index')
    success_message = texts.delete_user['delete_success']

    extra_context = {
        'base': texts.base,
        'delete_user': texts.delete_user,
    }

    def has_permission(self):
        return self.get_object().id == self.request.user.id

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, texts.auth['auth_required'])
            return redirect(reverse_lazy('login'))

        messages.error(self.request, texts.auth['permission_required'])
        return redirect(reverse_lazy('users_index'))
