import django.utils.timezone
from django.db import migrations, models


def set_content_default(apps, schema_editor):
    """Set content to empty string where NULL."""
    Note = apps.get_model("notes", "Note")
    Note.objects.filter(content__isnull=True).update(content="")


class Migration(migrations.Migration):
    dependencies = [
        ("notes", "0006_rename_user_id_note_user"),
    ]

    operations = [
        # Rename subject -> title
        migrations.RenameField(
            model_name="note",
            old_name="subject",
            new_name="title",
        ),
        migrations.AlterField(
            model_name="note",
            name="title",
            field=models.CharField(max_length=255, null=True),
        ),
        # Rename note -> content
        migrations.RenameField(
            model_name="note",
            old_name="note",
            new_name="content",
        ),
        # Set NULL content to empty string before changing default
        migrations.RunPython(set_content_default, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="note",
            name="content",
            field=models.TextField(blank=True, default=""),
        ),
        # Add timestamps
        migrations.AddField(
            model_name="note",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="note",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        # Remove selected field
        migrations.RemoveField(
            model_name="note",
            name="selected",
        ),
        # Add ordering
        migrations.AlterModelOptions(
            name="note",
            options={"ordering": ["-updated_at"]},
        ),
    ]
