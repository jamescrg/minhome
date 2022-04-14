
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import config.settings_local


asset_list = [
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


def fetch(symbol):
    """Fetch securities data for a specific symbol/asset"""

    url = 'https://finnhub.io/api/v1/quote'
    params = {
        'symbol': symbol,
        'token': config.settings_local.FINNHUB_API_KEY,
    }
    response = requests.get(url, params=params)
    quote = response.json()
    return quote


def collect(assets):
    """Fetch securities data for a list of symbols/assets"""

    for asset in assets:
        quote = fetch(asset['symbol'])
        asset['previous_close'] = quote['pc']
        asset['open'] = quote['o']
        asset['high'] = quote['h']
        asset['low'] = quote['l']
        asset['price'] = quote['c']
        asset['change'] = quote['d']
        asset['percent_change'] = quote['dp']
    return assets


def sort(data, ord):
    if (ord == 'percent_change'):
        reverse = True
    else:
        reverse = False
    sorted_data = sorted(data, key=lambda k: k[ord], reverse=reverse)
    return sorted_data
