from django.db import models
from accounts.models import CustomUser

class Event(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    description = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.description} : {self.id}'

    class Meta:
        db_table = 'app_event'
