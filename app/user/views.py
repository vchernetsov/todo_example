from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from user.permissions import IsOwner

from .models import User
from .serializers import UsersSerializer


class UserView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
               viewsets.GenericViewSet):
    """Get, list and update users"""

    queryset = User.objects.rendered()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    class Meta:
        model = User
