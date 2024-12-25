from django.test import TestCase
from django.test.client import Client
from django.urls import reverse_lazy

from task_manager import texts
from task_manager.factories import UserFactory


class SetUpMixin:
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()


class TestIndex(SetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.common_urls = [
            'index',
            'users_index',
        ]
        self.logged_in_urls = [
            'logout',
            'statuses_index',
            'labels_index',
            'tasks_index',
        ]
        self.logged_out_urls = [
            'login',
            'user_create',
        ]

    def test_navbar_without_login(self):
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

        # Check common elements
        self.assertContains(response, texts.base['logo_alt'])
        for url in self.common_urls:
            self.assertContains(response, reverse_lazy(url))

        # Check logged out specific elements
        for url in self.logged_out_urls:
            self.assertContains(response, reverse_lazy(url))

        # Check logged in elements should not be present
        for url in self.logged_in_urls:
            self.assertNotContains(response, reverse_lazy(url))

    def test_navbar_with_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')

        # Check common elements
        self.assertContains(response, texts.base['logo_alt'])
        for url in self.common_urls:
            self.assertContains(response, reverse_lazy(url))

        # Check logged in specific elements
        for url in self.logged_in_urls:
            self.assertContains(response, reverse_lazy(url))

        # Check logged out elements should not be present
        for url in self.logged_out_urls:
            self.assertNotContains(response, reverse_lazy(url))


class TestLogin(SetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.password = 'testpass!123'

    def test_login_form(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='login.html')
        self.assertContains(response, texts.base['login'])
        self.assertContains(response, texts.login['login_button'])

    def test_login_success(self):
        response = self.client.post(
            reverse_lazy('login'),
            {'username': self.user.username, 'password': self.password},
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('index'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, texts.login['login_success'])

    def test_login_failure(self):
        response = self.client.post(
            reverse_lazy('login'),
            {'username': self.user.username, 'password': 'wrong_password'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class TestLogout(SetUpMixin, TestCase):
    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse_lazy('logout'), follow=True)
        self.assertRedirects(response, reverse_lazy('index'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, texts.logout['logout_info'])
