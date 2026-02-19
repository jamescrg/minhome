"""Data migration to clear expanded_folders on all users."""

from django.db import migrations


def clear_expanded_folders(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    CustomUser.objects.all().update(expanded_folders={})


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0015_customuser_expanded_folders"),
    ]

    operations = [
        migrations.RunPython(clear_expanded_folders, migrations.RunPython.noop),
    ]
