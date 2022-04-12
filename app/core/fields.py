import uuid

from django.db import models


def UUIDPKField(**kwargs):
    return models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, **kwargs)
