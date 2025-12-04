from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import CustomUser


class Folder(models.Model):
    """A folder for categorizing favorites, contacts, notes or other data.

    Attributes:
        id (int): the unique identifier for the folder
        user (int): the user who created and owns the folder
        page (str): the page to which the folder belongs
        name (str): the name or title of the folder
        parent (Folder): the parent folder (for hierarchy)
        depth (int): the depth level (0=root, 1=child, 2=grandchild)
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
        CustomUser, on_delete=models.CASCADE, related_name="folder_owner"
    )
    page = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    depth = models.IntegerField(default=0)
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

    class Meta:
        db_table = "app_folder"

    def get_ancestors(self):
        """Return list of ancestor folders from root to immediate parent."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors

    def get_descendants(self):
        """Return all descendants (children, grandchildren) recursively."""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    def get_root(self):
        """Return the root folder of this hierarchy."""
        if self.parent is None:
            return self
        return self.parent.get_root()

    def get_full_path(self):
        """Return full path string like 'Parent / Child / Grandchild'."""
        ancestors = self.get_ancestors()
        path_parts = [f.name for f in ancestors] + [self.name]
        return " / ".join(path_parts)

    def can_have_children(self):
        """Check if this folder can accept child folders (depth < 2)."""
        return self.depth < 2

    def clean(self):
        """Validate depth constraints and prevent circular references."""
        if self.parent:
            # Prevent self-reference
            if self.pk and self.parent.pk == self.pk:
                raise ValidationError("A folder cannot be its own parent.")

            # Check for circular reference in ancestors
            current = self.parent
            while current:
                if self.pk and current.pk == self.pk:
                    raise ValidationError("Circular reference detected.")
                current = current.parent

            # Enforce max depth of 3 levels (0, 1, 2)
            if self.parent.depth >= 2:
                raise ValidationError("Cannot create folders beyond 3 levels deep.")

            # Set depth based on parent
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def update_descendant_depths(self):
        """Update depth for all descendants after a move operation."""
        for child in self.children.all():
            child.depth = self.depth + 1
            child.save(update_fields=["depth"])
            child.update_descendant_depths()


class UserFolderPosition(models.Model):
    """Track where a shared folder appears in a user's hierarchy.

    This allows shared folder recipients to position shared folders
    anywhere in their own folder hierarchy without affecting the
    original owner's structure.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="folder_positions"
    )
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="user_positions"
    )
    local_parent = models.ForeignKey(
        Folder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="positioned_children",
    )

    class Meta:
        db_table = "app_user_folder_position"
        unique_together = ("user", "folder")
