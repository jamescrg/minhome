from django.db import models
from django.utils import timezone


class TimestampMixin(models.Model):
    """Abstract mixin providing created_at and updated_at fields."""

    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
