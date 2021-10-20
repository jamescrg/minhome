
from django.db import models
from accounts.models import CustomUser


class Folder(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    page = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    home_column = models.IntegerField(blank=True, null=True)
    home_rank = models.IntegerField(blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    fillable = [
        'name',
        'home_column',
        'home_rank',
        'selected',
        'active',
    ]

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'app_folder'
