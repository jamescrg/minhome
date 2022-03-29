
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import config.settings_local
import apps.finance.crypto_data as crypto_data


@login_required
def crypto(request, ord='market_cap'):

    # specify the list of assets to be viewed
    symbols = 'ALGO,ATOM,BTC,ETH,IMX,MATIC,SOL,LRC,XCH,XLM,XMR'

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
def securities(request):

    assets = [
        {
            'symbol': 'GME',
            'exchange': 'NYSE',
            'name': 'Gamestop',
        },
        {
            'symbol': 'TSLA',
            'exchange': 'NASDAQ',
            'name': 'Tesla',
        },
        {
            'symbol': 'TLRY',
            'exchange': 'NASDAQ',
            'name': 'Tilray',
        },
        {
            'symbol': 'SNDL',
            'exchange': 'NASDAQ',
            'name': 'Sundial',
        },
    ]

    for asset in assets:

        url = 'https://finnhub.io/api/v1/quote'
        params = {
            'symbol': asset['symbol'],
            'token': config.settings_local.FINNHUB_API_KEY,
        }
        response = requests.get(url, params=params)
        result = response.json()

        asset['previous_close'] = result['pc']
        asset['open'] = result['o']
        asset['high'] = result['h']
        asset['low'] = result['l']
        asset['price'] = result['c']
        asset['change'] = result['d']
        asset['percent_change'] = result['dp']

    context = {
        'page': 'securities',
        'assets': assets,
    }
    return render(request, 'finance/securities.html', context)


@login_required
def positions(request):

    context = {
        'page': 'securities',
    }
    return render(request, 'finance/positions.html', context)
