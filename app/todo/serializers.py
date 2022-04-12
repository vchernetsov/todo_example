from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task object."""

    read_only_fields = ['uuid']

    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
        )

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
