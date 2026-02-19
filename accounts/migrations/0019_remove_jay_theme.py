"""Data migration to remove jay theme, falling back to matcha default."""

from django.db import migrations


def remove_jay_theme(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    CustomUser.objects.filter(theme="jay").update(theme="")


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0018_customuser_encryption_salt"),
    ]

    operations = [
        migrations.RunPython(remove_jay_theme, migrations.RunPython.noop),
    ]
