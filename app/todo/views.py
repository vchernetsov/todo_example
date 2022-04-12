from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from todo.models import Task
from todo.permissions import IsOwner
from todo.serializers import TaskSerializer


class TaskView(viewsets.ModelViewSet):
    """Manage tasks"""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    class Meta:
        model = Task

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(owner=user)
