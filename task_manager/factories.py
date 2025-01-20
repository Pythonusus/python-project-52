"""
Factories for generating test data.
"""
import factory
import factory.random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

# Set seed for random data generation to ensure consistent
# test data across different test runs.
SEED = 4321
factory.random.reseed_random(SEED)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    # Users in tests are always created with the same hashed password
    password = factory.LazyFunction(lambda: make_password('testpass!123'))


class StatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status

    name = factory.Sequence(lambda n: f'Status {n}')


class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    name = factory.Sequence(lambda n: f'Label {n}')


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Sequence(lambda n: f'Task {n}')
    description = factory.Faker('sentence')
    status = factory.SubFactory(StatusFactory)
    author = factory.SubFactory(UserFactory)
    executor = factory.SubFactory(UserFactory)

    @factory.post_generation
    def labels(self, created, extracted):
        """
        Post-generation hook for handling task labels.

        Args:
            created (bool): Whether the task was created successfully
            extracted (iterable, optional): Labels sequence to add to the task
            **kwargs: Additional arguments passed to the hook
        """
        if not created:
            return

        if extracted:
            # Add the provided labels to the task
            self.labels.set(extracted)
        else:
            # Create and add a default label
            label = LabelFactory()
            self.labels.add(label)
