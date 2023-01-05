
from django.db import models

from accounts.models import CustomUser
from apps.folders.models import Folder


class Contact(models.Model):
    """A person or entity and its associated contact information.

    Attributes:
        id (int): the unique identifier for the contact
        user (int): the user who created and owns the contact
        folder (int): the folder to which the contact belongs
        selected (int): whether the contact has been selected to be displayed
        name (str): the contact's full name
        company (str): if a person, their affiliated company
        address (str): full street address
        phone1 (str): primary phone
        phone1_label (str): primary phone label
        phone2 (str): seciondary phone
        phone2_label (str): seciondary phone label
        phone3 (str): tertiary phone
        phone3_label (str): tertiary phone label
        email (str): email address
        website (str): web address
        map (str): a url to google maps for the contact's address
        notes (str): comments about the contact
        google_id (str): if added to a Google account, the unique identifier for that Google contact
        fillable (list): a list of the above attributes that are fillable by a form
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone1 = models.CharField(max_length=50, blank=True, null=True)
    phone1_label = models.CharField(max_length=10, blank=True, null=True)
    phone2 = models.CharField(max_length=50, blank=True, null=True)
    phone2_label = models.CharField(max_length=10, blank=True, null=True)
    phone3 = models.CharField(max_length=50, blank=True, null=True)
    phone3_label = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    map = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True)

    fillable = [
        'folder_id',
        'name',
        'company',
        'address',
        'phone1',
        'phone1_label',
        'phone2',
        'phone2_label',
        'phone3',
        'phone3_label',
        'email',
        'website',
        'map',
        'notes',
    ]

    def __str__(self):
        return f'{self.name} : {self.id}'

    class Meta:
        db_table = 'app_contact'
