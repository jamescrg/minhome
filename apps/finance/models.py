from django.db import models

from accounts.models import CustomUser
from apps.common.models import TimestampMixin


class CryptoSymbol(TimestampMixin, models.Model):
    """A cryptocurrency symbol that a user wants to track.

    Attributes:
        user (ForeignKey): The user who owns this crypto symbol
        symbol (str): The crypto symbol (e.g., 'BTC', 'ETH')
        name (str): Full name of the cryptocurrency (e.g., 'Bitcoin', 'Ethereum')
        is_active (bool): Whether this symbol should be included in API calls
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="crypto_symbols"
    )
    symbol = models.CharField(max_length=20, help_text="Crypto symbol (e.g., BTC, ETH)")
    name = models.CharField(
        max_length=100, blank=True, help_text="Full name (e.g., Bitcoin)"
    )
    is_active = models.BooleanField(
        default=True, help_text="Include in crypto data calls"
    )

    class Meta:
        db_table = "finance_crypto_symbol"
        unique_together = ["user", "symbol"]
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} ({self.user.username})"


class SecuritiesSymbol(TimestampMixin, models.Model):
    """A securities symbol that a user wants to track.

    Attributes:
        user (ForeignKey): The user who owns this securities symbol
        symbol (str): The securities symbol (e.g., 'TSLA', 'GME')
        name (str): Full name of the security (e.g., 'Tesla', 'GameStop')
        exchange (str): Exchange where the security is traded (e.g., 'NYSE', 'NASDAQ')
        is_active (bool): Whether this symbol should be included in API calls
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="securities_symbols"
    )
    symbol = models.CharField(
        max_length=20, help_text="Securities symbol (e.g., TSLA, GME)"
    )
    name = models.CharField(max_length=100, help_text="Full name (e.g., Tesla)")
    exchange = models.CharField(
        max_length=20, help_text="Exchange (e.g., NYSE, NASDAQ)"
    )
    is_active = models.BooleanField(
        default=True, help_text="Include in securities data calls"
    )

    class Meta:
        db_table = "finance_securities_symbol"
        unique_together = ["user", "symbol"]
        ordering = ["symbol"]

    def __str__(self):
        return f"{self.symbol} ({self.user.username})"
