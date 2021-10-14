from django.db import models
from apps.folders.models import Folder


class Note(models.Model):

    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField()
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)
    fillable = [
        'folder_id',
        'subject',
        'note',
    ]

    def __str__(self):
        return f'{self.subject} : {self.id}'

    class Meta:
        db_table = 'app_note'

