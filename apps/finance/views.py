from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import apps.finance.crypto_data as crypto_data
import apps.finance.securities_data as securities_data
from django.conf import settings
from .models import CryptoSymbol, SecuritiesSymbol


@login_required
def crypto(request, ord="market_cap"):
    """Retrieve and display crypto data.

    Args:
    ord (str): the sort order for the list of assets,

    """

    # Get user's custom symbols only
    user_symbols = CryptoSymbol.objects.filter(user=request.user, is_active=True)
    
    if user_symbols.exists():
        # Use user's custom symbols
        symbols = ",".join([symbol.symbol for symbol in user_symbols])
        
        # collect data from remote service
        data = crypto_data.collect(symbols)

        # condense and sort the data
        data = crypto_data.condense(data)

        # sort the data according to the user indicated field
        # defaults to 'market cap', as specified above
        data = crypto_data.sort(data, ord=ord)
    else:
        # No symbols configured - show empty state
        data = []

    context = {
        "page": "crypto",
        "ord": ord,
        "data": data,
    }
    return render(request, "finance/crypto.html", context)


@login_required
def securities(request, ord="name"):
    """Retrieve and display securities data.

    Args:
        ord (str): the sort order for the list of assets,
            e.g. name, symbol, price, etc., with the default being name

    """

    # Get user's custom symbols only
    user_symbols = SecuritiesSymbol.objects.filter(user=request.user, is_active=True)
    
    if user_symbols.exists():
        # Convert user symbols to the format expected by securities_data.collect
        asset_list = []
        for symbol in user_symbols:
            asset_list.append({
                "symbol": symbol.symbol,
                "name": symbol.name,
                "exchange": symbol.exchange,
            })
        
        # Collect data from remote service
        data = securities_data.collect(asset_list)
        
        # Sort the data according to the user indicated field
        data = securities_data.sort(data, ord)
    else:
        # No symbols configured - show empty state
        data = []

    context = {
        "page": "securities",
        "ord": ord,
        "data": data,
    }
    return render(request, "finance/securities.html", context)


@login_required
def positions(request):
    """Retrieve and display positions in all assets.

    Notes:
        this function is currently unfinished and is not in active use

    """

    context = {
        "page": "securities",
    }
    return render(request, "finance/positions.html", context)
