# Generated by Django 3.2.6 on 2022-09-01 15:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("favorites", "0005_rename_user_id_favorite_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favorite",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
