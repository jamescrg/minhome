# Generated by Django 4.1.5 on 2023-03-07 14:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="preferences",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
