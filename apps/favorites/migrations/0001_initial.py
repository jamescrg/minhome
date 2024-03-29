# Generated by Django 3.2.6 on 2021-10-13 22:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("user_id", models.PositiveBigIntegerField()),
                ("folder_id", models.BigIntegerField(blank=True, null=True)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("url", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("login", models.CharField(blank=True, max_length=50, null=True)),
                ("root", models.CharField(blank=True, max_length=50, null=True)),
                ("passkey", models.CharField(blank=True, max_length=50, null=True)),
                ("selected", models.IntegerField(blank=True, null=True)),
                ("home_rank", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "app_favorite",
            },
        ),
    ]
