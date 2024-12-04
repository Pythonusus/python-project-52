from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from task_manager.users.forms import UserForm
from task_manager.users.models import User
from task_manager.texts import base, create_user


class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    extra_context = {
        'base': base,
    }


class UserCreateView(CreateView, SuccessMessageMixin):
    model = User
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = create_user['register_success']
    extra_context = {
        'base': base,
        'create_user': create_user,
    }
