# Generated by Django 3.2.6 on 2021-10-20 10:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("favorites", "0003_alter_favorite_folder"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="favorite",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
