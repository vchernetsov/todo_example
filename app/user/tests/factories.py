import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """User model factory"""

    username = factory.Sequence(lambda x: f'user_{x}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.LazyAttribute(lambda obj: f'first_{obj.username}')
    last_name = factory.LazyAttribute(lambda obj: f'last_{obj.username}')

    class Meta:
        model = User
