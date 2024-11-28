from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class UsersView(TemplateView):
    template_name = 'users.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class SignUpView(TemplateView):
    template_name = 'sign_up.html'
