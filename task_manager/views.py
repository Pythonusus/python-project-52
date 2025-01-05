from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

import task_manager.texts as texts


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {
        'base': texts.base,
    }


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Login user using Django's built-in authentication form.
    Redirects to the index page after successful login.
    Shows a success message after successful login.
    """
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_message = texts.login['login_success']
    next_page = reverse_lazy('index')
    extra_context = {
        'base': texts.base,
        'login': texts.login,
    }


class UserLogoutView(LogoutView):
    """
    Logout user using Django's built-in logout view.
    Redirects to the index page after successful logout.
    Shows an info message after successful logout.
    """
    next_page = reverse_lazy('index')
    extra_context = {
        'base': texts.base,
        'logout': texts.logout,
    }

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, texts.logout['logout_info'])
        return super().dispatch(request, *args, **kwargs)
