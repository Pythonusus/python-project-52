from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(LoginView):
    template_name = 'login.html'


class LogoutView(LogoutView):
    template_name = 'logout.html'
