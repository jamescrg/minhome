from django.db import models

from accounts.models import CustomUser


class Folder(models.Model):
    """A folder for categorizing favorites, contacts, notes or other data.

    Attributes:
        id (int): the unique identifier for the folder
        user (int): the user who created and owns the folder
        page (str): the page to which the folder belongs
        name (str): the name or title of the folder
        parent (Folder): parent folder for nesting (optional)
        home_column (int): whether the folder should be displayed on the home page, and
            if so, what rank it should have within its folder
        home_rank (int): whether the folder should be displayed on the home page, and
            if so, what rank it should have within its folder
        selected (int): for tasks folders,
            whether the folder has been selected to be displayed
        active (int): for task folders,
            whether the folder is active for new task entries
        editors: the list of users with access to edit the contents of the folder
    """

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="folder_owner")
    page = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", 
        blank=True, null=True, db_index=True)
    home_column = models.IntegerField(blank=True, null=True)
    home_rank = models.IntegerField(blank=True, null=True)
    selected = models.IntegerField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    editors = models.ManyToManyField(CustomUser, related_name="folder_editors")

    fillable = [
        "name",
        "parent",
        "home_column",
        "home_rank",
        "selected",
        "active",
    ]

    def __str__(self):
        return f"{self.name}"
    
    def get_ancestors(self):
        """Get all parent folders up to root."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors
    
    def get_descendants(self):
        """Get all child folders recursively."""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    class Meta:
        db_table = "app_folder"
