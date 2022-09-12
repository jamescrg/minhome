
from django.db import models
from apps.folders.models import Folder
from accounts.models import CustomUser


class Task(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200, null=True)
    status = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.title} : {self.id}'

    class Meta:
        db_table = 'app_task'
