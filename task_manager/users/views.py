from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView

from task_manager.users.models import User
from task_manager.texts import base, create_user


class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    extra_context = {
        'base': base,
    }


class UserCreateView(CreateView):
    model = User
    template_name = 'users/create.html'
    form_class = UserCreationForm
