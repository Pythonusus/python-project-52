from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.texts import base


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'base': base,
    }


class LoginView(LoginView):
    template_name = 'login.html'
    extra_context = {
        'base': base,
    }


class LogoutView(LogoutView):
    template_name = 'logout.html'
    extra_context = {
        'base': base,
    }
