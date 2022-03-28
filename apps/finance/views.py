
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import config.settings_local
import apps.finance.crypto_data as crypto_data


@login_required
def crypto(request, ord='market_cap'):

    # load the list of crypto positions
    positions = crypto_data.positions()

    # get the list of symbols as a string
    symbols = crypto_data.symbols(positions)

    # fetch data from remote service
    data = crypto_data.fetch(symbols)

    # fetch current crypto data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': symbols,
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

    cdata = []
    for sym in params['symbol'].split(','):
        result['data'][sym]['quote']['USD']['position'] = crypto_positions[sym]
        result['data'][sym]['quote']['USD']['position_value'] = crypto_positions[sym] * result['data'][sym]['quote']['USD']['price']
        cdata.append(result['data'][sym])

    cdata = sorted(
            cdata, key=lambda k: k['quote']['USD'][ord], reverse=True)

    total = 0
    for token in cdata:
        token['quote']['USD']['market_cap'] /= 1000000000
        total += token['quote']['USD']['position_value']

    # import config.helpers as helpers
    # return helpers.dump(cdata)

    context = {
        'page': 'crypto',
        'ord': ord,
        'crypto_data': cdata,
        'total': total,
    }
    return render(request, 'crypto/content.html', context)


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

    user_id = request.user.id

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


@login_required
def positions(request):

    context = {
        'page': 'securities',
    }
    return render(request, 'finance/positions.html', context)
