from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
from apps.folders.models import Folder


class Note(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=255, null=True)
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = "app_note"
        ordering = ["-updated_at"]
