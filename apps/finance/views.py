from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import apps.finance.crypto_data as crypto_data
import apps.finance.securities_data as securities_data
from django.conf import settings


@login_required
def crypto(request, ord="market_cap"):
    """Retrieve and display crypto data.

    Args:
    ord (str): the sort order for the list of assets,

    """

    # specify the list of assets to be viewed
    symbols = settings.CRYPTO_SYMBOLS

    # collect data from remote service
    data = crypto_data.collect(symbols)

    # condense and sort the data
    data = crypto_data.condense(data)

    # sort the data according to the user indicated field
    # defaults to 'market cap', as specified above
    data = crypto_data.sort(data, ord=ord)

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
        ord (int): the sort order for the list of assets,
            e.g. name, market cap, etc., with the default being name

    """

    asset_list = securities_data.asset_list
    data = securities_data.collect(asset_list)
    data = securities_data.sort(data, ord)

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
