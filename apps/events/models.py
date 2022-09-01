from django.db import models


class Event(models.Model):

    user_id = models.IntegerField(null=True)
    date = models.DateField(null=True)
    description = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.description} : {self.id}'

    class Meta:
        db_table = 'app_event'
