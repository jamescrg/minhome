from django import forms
from django.core.exceptions import ValidationError
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from .models import CryptoSymbol, SecuritiesSymbol
from django.conf import settings


class CryptoSymbolForm(forms.ModelForm):
    class Meta:
        model = CryptoSymbol
        fields = ['symbol', 'name', 'is_active']
        widgets = {
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., BTC, ETH',
                'style': 'text-transform: uppercase;'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Bitcoin (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def clean_symbol(self):
        symbol = self.cleaned_data['symbol'].upper().strip()
        
        if not symbol:
            raise ValidationError("Symbol is required.")
        
        if len(symbol) > 20:
            raise ValidationError("Symbol must be 20 characters or less.")
        
        # Check if symbol already exists for this user (if editing, exclude current instance)
        user = getattr(self.instance, 'user', None)
        if user:
            existing = CryptoSymbol.objects.filter(user=user, symbol=symbol)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError(f"You already have {symbol} in your list.")
        
        # Validate symbol against CoinMarketCap API
        if not self._validate_symbol_with_api(symbol):
            raise ValidationError(f"Symbol '{symbol}' not found in CoinMarketCap. Please check the symbol and try again.")
        
        return symbol
    
    def _validate_symbol_with_api(self, symbol):
        """Validate that the symbol exists in CoinMarketCap API"""
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        params = {
            "symbol": symbol,
            "convert": "USD",
            "CMC_PRO_API_KEY": settings.CRYPTO_API_KEY,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Check if the symbol was found
            if response.status_code == 200 and 'data' in data and symbol in data['data']:
                # Optionally, extract the name from the API response
                if not self.cleaned_data.get('name'):
                    crypto_data = data['data'][symbol]
                    self.cleaned_data['name'] = crypto_data.get('name', '')
                return True
            else:
                return False
                
        except (ConnectionError, Timeout, TooManyRedirects, Exception):
            # If API is down or unreachable, allow the symbol to be added
            # (you might want to change this behavior based on your preferences)
            return True


class SecuritiesSymbolForm(forms.ModelForm):
    class Meta:
        model = SecuritiesSymbol
        fields = ['symbol', 'name', 'exchange', 'is_active']
        widgets = {
            'symbol': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., TSLA, GME',
                'style': 'text-transform: uppercase;'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Tesla'
            }),
            'exchange': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., NYSE, NASDAQ'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def clean_symbol(self):
        symbol = self.cleaned_data['symbol'].upper().strip()
        
        if not symbol:
            raise ValidationError("Symbol is required.")
        
        if len(symbol) > 20:
            raise ValidationError("Symbol must be 20 characters or less.")
        
        # Check if symbol already exists for this user (if editing, exclude current instance)
        user = getattr(self.instance, 'user', None)
        if user:
            existing = SecuritiesSymbol.objects.filter(user=user, symbol=symbol)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise ValidationError(f"You already have {symbol} in your list.")
        
        # Validate symbol against Finnhub API
        if not self._validate_symbol_with_api(symbol):
            raise ValidationError(f"Symbol '{symbol}' not found in Finnhub. Please check the symbol and try again.")
        
        return symbol
    
    def _validate_symbol_with_api(self, symbol):
        """Validate that the symbol exists in Finnhub API"""
        url = "https://finnhub.io/api/v1/quote"
        params = {
            "symbol": symbol,
            "token": settings.FINNHUB_API_KEY,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            # Check if the symbol was found (Finnhub returns 0 values for invalid symbols)
            if response.status_code == 200 and 'c' in data and data['c'] != 0:
                return True
            else:
                return False
                
        except (ConnectionError, Timeout, TooManyRedirects, Exception):
            # If API is down or unreachable, allow the symbol to be added
            return True