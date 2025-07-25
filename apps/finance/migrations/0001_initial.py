# Generated by Django 4.2.11 on 2025-07-10 17:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CryptoSymbol",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "symbol",
                    models.CharField(
                        help_text="Crypto symbol (e.g., BTC, ETH)", max_length=20
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Full name (e.g., Bitcoin)",
                        max_length=100,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Include in crypto data calls"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crypto_symbols",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "finance_crypto_symbol",
                "ordering": ["symbol"],
                "unique_together": {("user", "symbol")},
            },
        ),
    ]
