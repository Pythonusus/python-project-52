from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager import texts
from task_manager.factories import StatusFactory, TaskFactory, UserFactory
from task_manager.statuses.models import Status


class SetUpMixin:
    def setUp(self):
        self.client = Client()
        self.statuses = StatusFactory.create_batch(3)
        self.user = UserFactory()
        self.client.force_login(self.user)


class TestStatusesCrudWithNoLogin(SetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_statuses_index_with_no_login(self):
        response = self.client.get(reverse_lazy('statuses_index'))
        expected_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('statuses_index')}"
        )
        self.assertRedirects(response, expected_url)

    def test_status_create_with_no_login(self):
        response = self.client.post(
            reverse_lazy('status_create'),
            {
                'name': 'New status',
            },
        )
        expected_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('status_create')}"
        )
        self.assertRedirects(response, expected_url)

    def test_status_update_with_no_login(self):
        response = self.client.post(
            reverse_lazy('status_update', args=[self.statuses[0].id]),
            {
                'name': 'Updated status',
            },
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('status_update', args=[self.statuses[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)

    def test_status_delete_with_no_login(self):
        response = self.client.post(
            reverse_lazy('status_delete', args=[self.statuses[0].id])
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('status_delete', args=[self.statuses[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)


class TestStatusesIndex(SetUpMixin, TestCase):
    def test_statuses_index(self):
        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/index.html')

        for text in texts.statuses_index.values():
            self.assertContains(response, text)

        for status in self.statuses:
            self.assertContains(response, status.name)
            self.assertContains(
                response,
                status.created_at.strftime('%d.%m.%Y %H:%M')
            )
            self.assertContains(
                response,
                reverse_lazy('status_update', args=[status.id])
            )
            self.assertContains(
                response,
                reverse_lazy('status_delete', args=[status.id])
            )


class TestStatusCreate(SetUpMixin, TestCase):
    def test_status_create_form(self):
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/create.html')
        self.assertContains(response, texts.create_status['create_status'])
        self.assertContains(response, texts.create_status['create'])

    def test_status_create_success(self):
        response = self.client.post(
            reverse_lazy('status_create'),
            {
                'name': 'New status',
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertContains(response, texts.create_status['create_success'])
        self.assertEqual(Status.objects.count(), 4)
        self.assertEqual(Status.objects.last().name, 'New status')

    def test_status_create_failure(self):
        response = self.client.post(
            reverse_lazy('status_create'),
            {
                'name': '',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('name', errors)


class TestStatusUpdate(SetUpMixin, TestCase):
    def test_status_update_form(self):
        response = self.client.get(
            reverse_lazy('status_update', args=[self.statuses[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/update.html')
        self.assertContains(response, texts.update_status['update_status'])
        self.assertContains(response, texts.update_status['update'])

    def test_status_update_success(self):
        response = self.client.post(
            reverse_lazy('status_update', args=[self.statuses[0].id]),
            {
                'name': 'New status',
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertContains(response, texts.update_status['update_success'])
        self.assertEqual(
            Status.objects.get(id=self.statuses[0].id).name, 'New status'
        )

    def test_status_update_failure(self):
        response = self.client.post(
            reverse_lazy('status_update', args=[self.statuses[0].id]),
            {
                'name': '',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('name', errors)


class TestStatusDelete(SetUpMixin, TestCase):
    def test_status_delete_form(self):
        response = self.client.get(
            reverse_lazy('status_delete', args=[self.statuses[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/delete.html')
        self.assertContains(response, texts.delete_status['delete_status'])
        self.assertContains(response, texts.delete_status['delete_confirm'])
        self.assertContains(response, texts.delete_status['delete_anyway'])

    def test_status_delete_success(self):
        response = self.client.post(
            reverse_lazy('status_delete', args=[self.statuses[0].id]),
            follow=True,
        )
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertContains(response, texts.delete_status['delete_success'])
        self.assertEqual(Status.objects.count(), 2)

    def test_status_delete_with_tasks_failure(self):
        TaskFactory.create(
            status=self.statuses[0],
            author=self.user,
            executor=self.user,
        )
        response = self.client.post(
            reverse_lazy('status_delete', args=[self.statuses[0].id]),
            follow=True,
        )
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertContains(response, texts.delete_status['delete_error'])
        self.assertEqual(Status.objects.count(), 3)
