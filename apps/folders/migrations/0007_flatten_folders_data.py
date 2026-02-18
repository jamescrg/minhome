"""Data migration to flatten folder hierarchy.

Sets parent=NULL and depth=0 on all folders, and deletes all UserFolderPosition rows.
"""

from django.db import migrations


def flatten_folders(apps, schema_editor):
    Folder = apps.get_model("folders", "Folder")
    Folder.objects.all().update(parent=None, depth=0)

    UserFolderPosition = apps.get_model("folders", "UserFolderPosition")
    UserFolderPosition.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("folders", "0006_add_folder_hierarchy"),
    ]

    operations = [
        migrations.RunPython(flatten_folders, migrations.RunPython.noop),
    ]
