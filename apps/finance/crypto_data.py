
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

import config.settings_local

def positions():
    return {
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


def symbols(positions):
    symbols = ''
    for key in positions.keys():
        symbols += ',' + key
    symbols = symbols[1:]
    return symbols


def fetch(symbols):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': symbols,
        'convert': 'USD',
        'CMC_PRO_API_KEY': config.settings_local.CRYPTO_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()['data']

    except (ConnectionError, Timeout, TooManyRedirects):
        result = None

    return result
