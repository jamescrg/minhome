# Generated by Django 3.2.6 on 2021-10-20 10:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("favorites", "0004_auto_20211020_1026"),
    ]

    operations = [
        migrations.RenameField(
            model_name="favorite",
            old_name="user_id",
            new_name="user",
        ),
    ]
