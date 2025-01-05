"""
Factories for generating test data.
"""
import factory
import factory.random
from task_manager.users.models import User
from django.contrib.auth.hashers import make_password

"""
Set seed for random data generation to ensure consistent
test data across different test runs.
"""
SEED = 4321
factory.random.reseed_random(SEED)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    # Users in tests are always created with the same hashed password
    password = factory.LazyFunction(lambda: make_password('testpass!123'))
