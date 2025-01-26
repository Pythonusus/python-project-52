from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager import texts
from task_manager.factories import (
    LabelFactory,
    StatusFactory,
    TaskFactory,
    UserFactory,
)
from task_manager.tasks.models import Task


class SetUpMixin:
    def setUp(self):
        self.client = Client()
        self.tasks = TaskFactory.create_batch(3)
        self.user = UserFactory()
        self.client.force_login(self.user)


class TestTasksCrudWithNoLogin(SetUpMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_tasks_index_with_no_login(self):
        response = self.client.get(reverse_lazy('tasks_index'))
        expected_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('tasks_index')}"
        )
        self.assertRedirects(response, expected_url)

    def test_task_create_with_no_login(self):
        response = self.client.post(
            reverse_lazy('task_create'),
            {
                'name': 'New task',
            },
        )
        expected_url = (
            f"{reverse_lazy('login')}?next={reverse_lazy('task_create')}"
        )
        self.assertRedirects(response, expected_url)

    def test_task_update_with_no_login(self):
        response = self.client.post(
            reverse_lazy('task_update', args=[self.tasks[0].id]),
            {
                'name': 'Updated task',
            },
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('task_update', args=[self.tasks[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)

    def test_task_delete_with_no_login(self):
        response = self.client.post(
            reverse_lazy('task_delete', args=[self.tasks[0].id])
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('task_delete', args=[self.tasks[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)

    def test_task_view_with_no_login(self):
        response = self.client.get(
            reverse_lazy('task_view', args=[self.tasks[0].id])
        )
        expected_url = (
            f"{
                reverse_lazy('login')}?next={
                reverse_lazy('task_view', args=[self.tasks[0].id])
            }"
        )
        self.assertRedirects(response, expected_url)


class TestTasksIndex(SetUpMixin, TestCase):
    def test_tasks_index(self):
        response = self.client.get(reverse_lazy('tasks_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

        for text in texts.tasks_index.values():
            self.assertContains(response, text)

        for task in self.tasks:
            self.assertContains(response, task.name)
            self.assertContains(response, task.status.name)
            self.assertContains(response, task.author.get_full_name())
            self.assertContains(response, task.executor.get_full_name())
            self.assertContains(
                response,
                task.created_at.strftime('%d.%m.%Y %H:%M')
            )
            self.assertContains(
                response,
                reverse_lazy('task_update', args=[task.id])
            )
            self.assertContains(
                response,
                reverse_lazy('task_delete', args=[task.id])
            )

    def test_tasks_index_with_filters(self):
        # Task that matches all filters and created by the logged-in user
        matching_task = TaskFactory(
            status=self.tasks[0].status,
            executor=self.tasks[0].executor,
            labels=self.tasks[0].labels.all(),
            author=self.user,
        )

        # Tasks that fail each filter condition
        wrong_status_task = TaskFactory(
            status=StatusFactory(),
            executor=self.tasks[0].executor,
            labels=self.tasks[0].labels.all(),
            author=self.user,
        )
        wrong_executor_task = TaskFactory(
            status=self.tasks[0].status,
            executor=UserFactory(),
            labels=self.tasks[0].labels.all(),
            author=self.user,
        )
        wrong_author_task = TaskFactory(
            status=self.tasks[0].status,
            executor=self.tasks[0].executor,
            labels=self.tasks[0].labels.all(),
            author=UserFactory(),
        )

        response = self.client.get(reverse_lazy('tasks_index'), {
            'status': self.tasks[0].status.id,
            'executor': self.tasks[0].executor.id,
            'labels': [label.id for label in self.tasks[0].labels.all()],
            'self_tasks': 'on',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, matching_task.name)

        self.assertNotContains(response, wrong_status_task.name)
        self.assertNotContains(response, wrong_executor_task.name)
        self.assertNotContains(response, wrong_author_task.name)


class TestTaskCreate(SetUpMixin, TestCase):
    def test_task_create_form(self):
        response = self.client.get(reverse_lazy('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create.html')
        self.assertContains(response, texts.create_task['create_task'])
        self.assertContains(response, texts.create_task['create'])

    def test_task_with_full_data_create_success(self):
        status = StatusFactory()
        labels = LabelFactory.create_batch(2)
        response = self.client.post(
            reverse_lazy('task_create'),
            {
                'name': 'New task',
                'description': 'New task description',
                'status': status.id,
                'labels': [label.id for label in labels],
                'executor': self.user.id,
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertContains(response, texts.create_task['create_success'])
        self.assertEqual(Task.objects.count(), 4)

        created_task = Task.objects.last()
        self.assertEqual(created_task.name, 'New task')
        self.assertEqual(created_task.description, 'New task description')
        self.assertEqual(created_task.status, status)
        self.assertEqual(created_task.labels.count(), 2)
        self.assertEqual(created_task.executor, self.user)
        self.assertEqual(created_task.author, self.user)

    def test_task_only_with_neccesary_data_create_success(self):
        status = StatusFactory()
        response = self.client.post(
            reverse_lazy('task_create'),
            {
                'name': 'New task',
                'status': status.id,
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertContains(response, texts.create_task['create_success'])
        self.assertEqual(Task.objects.count(), 4)

        created_task = Task.objects.last()
        self.assertEqual(created_task.name, 'New task')
        self.assertEqual(created_task.status, status)
        self.assertEqual(created_task.author, self.user)

    def test_task_create_failure(self):
        response = self.client.post(
            reverse_lazy('task_create'),
            {
                'name': self.tasks[0].name,
            },
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('name', errors)
        self.assertIn('status', errors)


class TestTaskUpdate(SetUpMixin, TestCase):
    def test_task_update_form(self):
        response = self.client.get(
            reverse_lazy('task_update', args=[self.tasks[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update.html')
        self.assertContains(response, texts.update_task['update_task'])
        self.assertContains(response, texts.update_task['update'])

    def test_task_update_success(self):
        response = self.client.post(
            reverse_lazy('task_update', args=[self.tasks[0].id]),
            {
                'name': 'Updated task',
                'status': self.tasks[0].status.id,
            },
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertContains(response, texts.update_task['update_success'])
        self.assertEqual(
            Task.objects.get(id=self.tasks[0].id).name,
            'Updated task'
        )

    def test_task_update_failure(self):
        response = self.client.post(
            reverse_lazy('task_update', args=[self.tasks[0].id]),
            {
                'name': '',
            },
        )
        self.assertEqual(response.status_code, 200)
        errors = response.context['form'].errors
        self.assertIn('name', errors)


class TestTaskDelete(SetUpMixin, TestCase):
    def test_task_delete_form(self):
        task = TaskFactory(author=self.user)
        response = self.client.get(
            reverse_lazy('task_delete', args=[task.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete.html')
        self.assertContains(response, texts.delete_task['delete_task'])
        self.assertContains(response, texts.delete_task['delete_confirm'])
        self.assertContains(response, texts.delete_task['delete_anyway'])

    def test_task_delete_success(self):
        task = TaskFactory(author=self.user)
        response = self.client.post(
            reverse_lazy('task_delete', args=[task.id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertContains(response, texts.delete_task['delete_success'])
        self.assertEqual(Task.objects.count(), 3)

    def test_task_delete_failure(self):
        response = self.client.post(
            reverse_lazy('task_delete', args=[self.tasks[0].id]),
            follow=True
        )
        self.assertRedirects(response, reverse_lazy('tasks_index'))
        self.assertContains(response, texts.delete_task['delete_error'])
        self.assertEqual(Task.objects.count(), 3)


class TestTaskView(SetUpMixin, TestCase):
    def test_task_view(self):
        response = self.client.get(
            reverse_lazy('task_view', args=[self.tasks[0].id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail.html')

        for text in texts.task_view.values():
            self.assertContains(response, text)

        self.assertContains(response, self.tasks[0].name)
        self.assertContains(response, self.tasks[0].description)
        self.assertContains(response, self.tasks[0].status.name)
        for label in self.tasks[0].labels.all():
            self.assertContains(response, label.name)
        self.assertContains(response, self.tasks[0].author.get_full_name())
        self.assertContains(response, self.tasks[0].executor.get_full_name())
        self.assertContains(
            response,
            self.tasks[0].created_at.strftime('%d.%m.%Y %H:%M')
        )
        self.assertContains(
            response,
            reverse_lazy('task_update', args=[self.tasks[0].id])
        )
        self.assertContains(
            response,
            reverse_lazy('task_delete', args=[self.tasks[0].id])
        )
