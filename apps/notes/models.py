from django.db import models


class Note(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField()
    folder_id = models.BigIntegerField(blank=True, null=True)
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

