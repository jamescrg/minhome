
from django.db import models
from apps.folders.models import Folder
from accounts.models import CustomUser


class Favorite(models.Model):

    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=50, blank=True, null=True)
    root = models.CharField(max_length=50, blank=True, null=True)
    passkey = models.CharField(max_length=50, blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)
    home_rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'app_favorite'
