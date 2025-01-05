"""
Factories for generating test data.
"""
import factory
import factory.random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

"""
Set seed for random data generation to ensure consistent
test data across different test runs.
"""
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
