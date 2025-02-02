from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager import texts
from task_manager.mixins import OwnershipRequiredMixin
from task_manager.users.forms import UserForm, UserUpdateForm


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
                     OwnershipRequiredMixin,
                     UpdateView):
    """
    Update a user. Users cannot update other users.
    Redirects to the users index page after successful update.
    Shows a success message after successful update.
    """
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'users/update.html'

    # OwnershipRequiredMixin settings
    ownership_field = 'user'
    permission_denied_message = texts.auth['permission_required']
    permission_denied_redirect_url = 'users_index'

    success_url = reverse_lazy('users_index')
    success_message = texts.update_user['update_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'update_user': texts.update_user,
    }


class UserDeleteView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     OwnershipRequiredMixin,
                     DeleteView):
    """
    Delete a user. Users cannot delete other users.
    Redirects to the users index page after successful deletion.
    Shows a success message after successful deletion.
    """
    model = get_user_model()
    template_name = 'users/delete.html'
    permission_required = 'auth.delete_user'

    # OwnershipRequiredMixin settings
    ownership_field = 'user'
    permission_denied_message = texts.auth['permission_required']
    permission_denied_redirect_url = 'users_index'

    success_url = reverse_lazy('users_index')
    success_message = texts.delete_user['delete_success']
    login_url = reverse_lazy('login')
    extra_context = {
        'base': texts.base,
        'delete_user': texts.delete_user,
    }
