
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import config.settings_local
import apps.finance.crypto_data as crypto_data
import apps.finance.securities_data as securities_data


@login_required
def crypto(request, ord='market_cap'):
    """View crypto data"""

    # specify the list of assets to be viewed
    symbols = 'ADA,ALGO,APE,ATOM,BTC,DOT,ETH,IMX,MATIC,SOL,SUSHI,LRC,XCH,XLM,XMR'

    # fetch data from remote service
    data = crypto_data.fetch(symbols)

    # condense and sort the data
    data = crypto_data.condense(data)

    # sort the data according to the user indicated field
    # defaults to 'market cap', as specified above
    data = crypto_data.sort(data, ord=ord)

    context = {
        'page': 'crypto',
        'ord': ord,
        'data': data,
    }
    return render(request, 'finance/crypto.html', context)


@login_required
def securities(request, ord='name'):
    """View securities data"""

    asset_list = securities_data.asset_list
    data = securities_data.collect(asset_list)
    data = securities_data.sort(data, ord)

    context = {
        'page': 'securities',
        'ord': ord,
        'data': data,
    }
    return render(request, 'finance/securities.html', context)


@login_required
def positions(request):
    """View positions for all assets"""

    context = {
        'page': 'securities',
    }
    return render(request, 'finance/positions.html', context)
