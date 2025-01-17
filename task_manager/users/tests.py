from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse_lazy

from task_manager import texts
from task_manager.factories import UserFactory


class TestUsersIndex(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = UserFactory.create_batch(5)

    def test_users_index(self):
        response = self.client.get(reverse_lazy('users_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/index.html')

        for text in texts.users_index.values():
            self.assertContains(response, text)

        for user in self.users:
            self.assertContains(response, user.username)
            self.assertContains(response, user.get_full_name())
            self.assertContains(
                response,
                user.date_joined.strftime('%d.%m.%Y %H:%M')
            )
            self.assertContains(
                response,
                reverse_lazy('user_update', args=[user.id])
            )
            self.assertContains(
                response,
                reverse_lazy('user_delete', args=[user.id])
            )


class TestUserCreate(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_create_form(self):
        response = self.client.get(reverse_lazy('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')
        self.assertContains(response, texts.create_user['registration'])
        self.assertContains(response, texts.create_user['register'])

    def test_user_create_success(self):
        response = self.client.post(
            reverse_lazy('user_create'),
            {
                'first_name': 'Vasya',
                'last_name': 'Pupkin',
                'username': 'testuserpupkin',
                'password1': 'testpass!123',
                'password2': 'testpass!123',
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertContains(response, texts.create_user['register_success'])
        User = get_user_model()
        created_user = User.objects.get(username='testuserpupkin')
        self.assertEqual(created_user.first_name, 'Vasya')
        self.assertEqual(created_user.last_name, 'Pupkin')

    def test_user_create_failure(self):
        response = self.client.post(
            reverse_lazy('user_create'),
            {
                'first_name': 'Vasya',
                'last_name': 'Pupkin',
                'username': '',
                'password1': 'testpass!123',
                'password2': 'testpass!123',
            },
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('username', errors)


class TestUserUpdate(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = UserFactory.create_batch(3)

    def test_user_update_with_login(self):
        self.client.force_login(self.users[0])
        response = self.client.get(
            reverse_lazy('user_update', args=[self.users[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/update.html')
        self.assertContains(response, texts.update_user['edit_user'])
        self.assertContains(response, texts.update_user['update'])
        response = self.client.post(
            reverse_lazy('user_update', args=[self.users[0].id]),
            {
                'first_name': 'Vasya',
                'last_name': 'Pupkin',
                'username': self.users[0].username,
                'password1': self.users[0].password,
                'password2': self.users[0].password,
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertContains(response, texts.update_user['update_success'])
        User = get_user_model()
        updated_user = User.objects.get(id=self.users[0].id)
        self.assertEqual(updated_user.first_name, 'Vasya')
        self.assertEqual(updated_user.last_name, 'Pupkin')

    def test_user_update_with_no_login(self):
        response = self.client.get(
            reverse_lazy('user_update', args=[self.users[0].id]),
            follow=True
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('user_update', args=[self.users[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)
        self.assertContains(response, texts.auth['auth_required'])

    def test_user_update_with_no_permission(self):
        self.client.force_login(self.users[1])
        response = self.client.get(
            reverse_lazy('user_update', args=[self.users[0].id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertContains(response, texts.auth['permission_required'])


class TestUserDelete(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = UserFactory.create_batch(3)

    def test_user_delete_with_login(self):
        self.client.force_login(self.users[0])
        response = self.client.get(
            reverse_lazy('user_delete', args=[self.users[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')
        self.assertContains(response, texts.delete_user['delete_user'])
        self.assertContains(response, texts.delete_user['delete_confirm'])
        self.assertContains(response, texts.delete_user['delete_anyway'])
        response = self.client.post(
            reverse_lazy('user_delete', args=[self.users[0].id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertContains(response, texts.delete_user['delete_success'])
        User = get_user_model()
        self.assertFalse(User.objects.filter(id=self.users[0].id).exists())

    def test_user_delete_with_no_login(self):
        response = self.client.get(
            reverse_lazy('user_delete', args=[self.users[0].id]),
            follow=True
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('user_delete', args=[self.users[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)
        self.assertContains(response, texts.auth['auth_required'])

    def test_user_delete_with_no_permission(self):
        self.client.force_login(self.users[1])
        response = self.client.get(
            reverse_lazy('user_delete', args=[self.users[0].id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('users_index'))
        self.assertContains(response, texts.auth['permission_required'])
