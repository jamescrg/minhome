
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

import config.settings_local


@login_required
def crypto(request, ord='market_cap'):

    positions = {
        'ALGO': 1000,
        'ATOM': 0.7903,
        'BTC': 0.7903,
        'ETH': 12,
        'IMX': 3500,
        'MATIC': 3000,
        'SOL': 10,
        'LRC': 997,
        'XCH': 0.5,
        'XLM': 11991,
        'XMR': 20,
    }

    key_string = ''
    for key in positions.keys():
        key_string += ',' + key
    key_string = key_string[1:]

    # fetch current crypto data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': key_string,
        'convert': 'USD',
        'CMC_PRO_API_KEY': config.settings_local.CRYPTO_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()
    except (ConnectionError, Timeout, TooManyRedirects):
        result = None

    # import config.helpers as helpers
    # return helpers.dump(result)

    crypto_data = []
    for sym in params['symbol'].split(','):
        result['data'][sym]['quote']['USD']['position'] = positions[sym]
        result['data'][sym]['quote']['USD']['position_value'] = positions[sym] * result['data'][sym]['quote']['USD']['price']
        crypto_data.append(result['data'][sym])

    crypto_data = sorted(
            crypto_data, key=lambda k: k['quote']['USD'][ord], reverse=True)

    total = 0
    for token in crypto_data:
        token['quote']['USD']['market_cap'] /= 1000000000
        total += token['quote']['USD']['position_value']

    # import config.helpers as helpers
    # return helpers.dump(crypto_data)

    context = {
        'page': 'crypto',
        'ord': ord,
        'crypto_data': crypto_data,
        'total': total,
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
