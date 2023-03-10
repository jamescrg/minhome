from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    google_credentials = models.TextField(null=True, blank=True)
    settings = models.JSONField(default=dict, blank=True)
    theme = models.TextField(default="", blank=True)
    search_engine = models.TextField(default="google", blank=True)
