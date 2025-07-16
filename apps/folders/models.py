from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

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
        CustomUser, on_delete=models.CASCADE, related_name="folder_owner"
    )
    page = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
        db_index=True,
    )
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

    def get_inherited_editors(self):
        """Get editors inherited from parent folders."""
        inherited_editors = set()
        for ancestor in self.get_ancestors():
            if ancestor.editors.exists():
                inherited_editors.update(ancestor.editors.all())
        return inherited_editors

    def has_inherited_access(self, user):
        """Check if user has access through parent folder sharing."""
        return user in self.get_inherited_editors()

    def is_shared_or_inherited(self):
        """Check if folder is shared directly or through inheritance."""
        return self.editors.exists() or len(self.get_inherited_editors()) > 0

    def propagate_permissions_to_descendants(self):
        """Propagate this folder's editor permissions to all descendants."""
        if not self.editors.exists():
            return

        editors_to_add = list(self.editors.all())
        descendants = self.get_descendants()

        for descendant in descendants:
            for editor in editors_to_add:
                descendant.editors.add(editor)

    def remove_inherited_permissions_from_descendants(self, editors_to_remove):
        """Remove inherited permissions from descendants when moving out of shared hierarchy."""
        descendants = self.get_descendants()

        for descendant in descendants:
            # Get inherited editors excluding this folder's contribution
            inherited_editors = set()
            for ancestor in descendant.get_ancestors():
                if ancestor != self and ancestor.editors.exists():
                    inherited_editors.update(ancestor.editors.all())

            for editor in editors_to_remove:
                # Only remove if the editor doesn't have access through:
                # 1. Direct sharing on the descendant itself
                # 2. Inheritance from other ancestors (not this folder)
                if (
                    descendant.editors.filter(pk=editor.pk).exists()
                    or editor in inherited_editors
                ):
                    continue
                else:
                    descendant.editors.remove(editor)

    def clean(self):
        """Validate folder constraints."""
        super().clean()

        # Check depth limit (3 levels maximum)
        if self.parent is not None:
            depth = len(self.parent.get_ancestors())
            if depth >= 2:  # 0-indexed: 0=root, 1=level1, 2=level2 (can't add level3)
                raise ValidationError("Cannot nest folders more than 3 levels deep.")

    def save(self, *args, **kwargs):
        """Save folder with validation."""
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "app_folder"


@receiver(m2m_changed, sender=Folder.editors.through)
def handle_folder_editors_changed(sender, instance, action, pk_set, **kwargs):
    """Handle changes to folder editors - propagate permissions to descendants."""
    if action == "post_add":
        # Editors were added to the folder
        instance.propagate_permissions_to_descendants()
    elif action == "post_remove":
        # Editors were removed from the folder
        if pk_set:
            from accounts.models import CustomUser

            editors_removed = CustomUser.objects.filter(pk__in=pk_set)
            instance.remove_inherited_permissions_from_descendants(editors_removed)
