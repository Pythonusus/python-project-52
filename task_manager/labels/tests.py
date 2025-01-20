from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager import texts
from task_manager.factories import LabelFactory, TaskFactory, UserFactory
from task_manager.labels.models import Label


class SetUpMixin:
    def setUp(self):
        self.client = Client()
        self.labels = LabelFactory.create_batch(3)
        self.user = UserFactory()
        self.client.force_login(self.user)


class TestLabelsCRUDWithNoLogin(SetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_labels_index_with_no_login(self):
        response = self.client.get(reverse_lazy('labels_index'))
        expected_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('labels_index')}"
        )
        self.assertRedirects(response, expected_url)

    def test_label_create_with_no_login(self):
        response = self.client.post(
            reverse_lazy('label_create'),
            {'name': 'New label'},
        )
        expected_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('label_create')}"
        )
        self.assertRedirects(response, expected_url)

    def test_label_update_with_no_login(self):
        response = self.client.post(
            reverse_lazy('label_update', args=[self.labels[0].id]),
            {'name': 'Updated label'},
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('label_update', args=[self.labels[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)

    def test_label_delete_with_no_login(self):
        response = self.client.post(
            reverse_lazy('label_delete', args=[self.labels[0].id])
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('label_delete', args=[self.labels[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)


class TestLabelsIndex(SetUpMixin, TestCase):
    def test_labels_index(self):
        response = self.client.get(reverse_lazy('labels_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/index.html')

        for text in texts.labels_index.values():
            self.assertContains(response, text)

        for label in self.labels:
            self.assertContains(response, label.name)
            self.assertContains(
                response,
                reverse_lazy('label_update', args=[label.id])
            )
            self.assertContains(
                response,
                reverse_lazy('label_delete', args=[label.id])
            )


class TestLabelCreate(SetUpMixin, TestCase):
    def test_label_create_form(self):
        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/create.html')
        self.assertContains(response, texts.create_label['create_label'])
        self.assertContains(response, texts.create_label['create'])

    def test_label_create_success(self):
        response = self.client.post(
            reverse_lazy('label_create'),
            {'name': 'New label'},
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('labels_index'))
        self.assertContains(response, texts.create_label['create_success'])
        self.assertEqual(Label.objects.count(), 4)

        created_label = Label.objects.last()
        self.assertEqual(created_label.name, 'New label')

    def test_label_create_failure(self):
        response = self.client.post(
            reverse_lazy('label_create'),
            {'name': ''},
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('name', errors)


class TestLabelUpdate(SetUpMixin, TestCase):
    def test_label_update_form(self):
        response = self.client.get(
            reverse_lazy('label_update', args=[self.labels[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/update.html')
        self.assertContains(response, texts.update_label['update_label'])
        self.assertContains(response, texts.update_label['update'])

    def test_label_update_success(self):
        response = self.client.post(
            reverse_lazy('label_update', args=[self.labels[0].id]),
            {'name': 'Updated label'},
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('labels_index'))
        self.assertContains(response, texts.update_label['update_success'])
        updated_label = Label.objects.get(id=self.labels[0].id)
        self.assertEqual(updated_label.name, 'Updated label')

    def test_label_update_failure(self):
        response = self.client.post(
            reverse_lazy('label_update', args=[self.labels[0].id]),
            {'name': ''},
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('name', errors)


class TestLabelDelete(SetUpMixin, TestCase):
    def test_label_delete_form(self):
        response = self.client.get(
            reverse_lazy('label_delete', args=[self.labels[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/delete.html')
        self.assertContains(response, texts.delete_label['delete_label'])
        self.assertContains(response, texts.delete_label['delete_confirm'])
        self.assertContains(response, texts.delete_label['delete_anyway'])

    def test_label_delete_success(self):
        response = self.client.post(
            reverse_lazy('label_delete', args=[self.labels[0].id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('labels_index'))
        self.assertContains(response, texts.delete_label['delete_success'])
        self.assertEqual(Label.objects.count(), 2)

    def test_label_with_tasks_delete_failure(self):
        TaskFactory(labels=[self.labels[0]])
        response = self.client.post(
            reverse_lazy('label_delete', args=[self.labels[0].id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('labels_index'))
        self.assertContains(response, texts.delete_label['delete_error'])
        self.assertEqual(Label.objects.count(), 3)
