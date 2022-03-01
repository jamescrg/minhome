
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

import config.settings_local


@login_required
def crypto(request, ord='market_cap'):

    # fetch current crypto data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': 'BTC,ETH,IMX,MATIC,XMR,SOL,LRC,XCH',
        'convert': 'USD',
        'CMC_PRO_API_KEY': config.settings_local.CRYPTO_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()
    except (ConnectionError, Timeout, TooManyRedirects):
        result = None

    crypto_data = []
    for sym in params['symbol'].split(','):
        crypto_data.append(result['data'][sym])

    crypto_data = sorted(
            crypto_data, key=lambda k: k['quote']['USD'][ord], reverse=True)

    for token in crypto_data:
        token['quote']['USD']['market_cap'] /= 1000000000

    # import config.helpers as helpers
    # return helpers.dump(crypto_data)

    context = {
        'page': 'crypto',
        'ord': ord,
        'crypto_data': crypto_data,
    }
    return render(request, 'crypto/content.html', context)


@login_required
def securities(request):
    user_id = request.user.id

    if user_id != 1:
        return redirect('/home/')

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

    # import config.helpers as helpers
    # return helpers.dump(assets)

    context = {
        'page': 'securities',
        'assets': assets,
    }
    return render(request, 'finance/content.html', context)
