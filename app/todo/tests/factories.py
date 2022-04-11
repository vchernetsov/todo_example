import factory

from todo.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    """Task model factory"""

    name = factory.Sequence(lambda x: f'task_name_{x}')
    description = factory.LazyAttribute(lambda obj: f'description_{obj.name}')

    class Meta:
        model = Task
