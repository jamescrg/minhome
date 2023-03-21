from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    zip = models.IntegerField(null=True, blank=True)
    google_credentials = models.TextField(null=True, blank=True)
    theme = models.TextField(default="", blank=True)
    search_engine = models.TextField(default="google", blank=True)
    home_events = models.IntegerField(default=0)
    home_events_hidden = models.DateField(null=True)
    home_tasks = models.IntegerField(default=0)
    home_tasks_hidden = models.DateField(null=True)
    home_search = models.IntegerField(default=0)
    favorites_folder = models.IntegerField(default=0)
    contacts_folder = models.IntegerField(default=0)
    contacts_contact = models.IntegerField(default=0)
    notes_folder = models.IntegerField(default=0)
    notes_note = models.IntegerField(default=0)
    tasks_folder = models.IntegerField(default=0)
    tasks_folders = models.JSONField(default=list)
    tasks_active_folder = models.IntegerField(default=0)
