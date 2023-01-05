
from django.db import models
from apps.folders.models import Folder
from accounts.models import CustomUser


class Note(models.Model):
    """A user's note, may be in plain text or markdown.

    Attributes:
        id (int): the unique identifier for the favorite
        user (int): the user who created and owns the note
        folder (int): the folder to which the note belongs
        subject (str): the subject matter of the note
        note (str): the content of the note
        selected (int): whether the favorite has been selected to be displayed
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=50, null=True)
    note = models.TextField(blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        db_table = 'app_note'

