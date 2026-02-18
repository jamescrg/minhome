from django.db import models

from accounts.models import CustomUser
from apps.common.models import TimestampMixin
from apps.folders.models import Folder


class Favorite(TimestampMixin, models.Model):
    """A favorite url belonging to the user.

    Attributes:
        id (int): the unique identifier for the favorite
        user (int): the user who created and owns the favorite
        folder (int): the folder to which the favorite belongs
        name (str): the name or title of the favorite url
        url (str): a web url
        description (str): a description of the site
        selected (int): whether the favorite has been selected to be displayed
        home_rank (int): whether the favorite should be displayed on the home page, and
            if so, what rank it should have within its folder
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)
    home_rank = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "app_favorite"
