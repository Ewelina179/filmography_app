import factory
from faker import Faker

fake = Faker()

from django.contrib.auth.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name
    email = fake.email
    password = fake.password
