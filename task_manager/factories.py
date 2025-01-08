"""
Factories for generating test data.
"""
import factory
import factory.random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

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


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Sequence(lambda n: f'Task {n}')
    description = factory.Faker('sentence')
    status = factory.SubFactory(StatusFactory)
    author = factory.SubFactory(UserFactory)
    executor = factory.SubFactory(UserFactory)
