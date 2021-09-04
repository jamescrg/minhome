from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    google_credentials = models.TextField(null=True, blank=True)
