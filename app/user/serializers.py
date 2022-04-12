from rest_framework import serializers

from .models import User


class UsersSerializer(serializers.ModelSerializer):
    """Serializer for user object."""

    read_only_fields = ['uuid']

    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'email',
            'first_name',
            'last_name',
        )
        read_only_fields = ['uuid']
