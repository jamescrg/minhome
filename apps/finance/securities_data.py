
import os

import requests
from dotenv import load_dotenv


asset_list = [
    {'symbol': 'GME', 'exchange': 'NYSE', 'name': 'Gamestop', },
    {'symbol': 'TSLA', 'exchange': 'NASDAQ', 'name': 'Tesla', },
    {'symbol': 'TLRY', 'exchange': 'NASDAQ', 'name': 'Tilray', },
    {'symbol': 'SNDL', 'exchange': 'NASDAQ', 'name': 'Sundial', },
    {'symbol': 'BBBY', 'exchange': 'NASDAQ', 'name': 'BBBY', },
    {'symbol': 'O', 'exchange': 'NYSE', 'name': 'REIT', },
    {'symbol': 'FXF', 'exchange': 'NYSEARCA', 'name': 'Swiss Francs', },
    {'symbol': 'GLD', 'exchange': 'NSEARCA', 'name': 'Gold ETF', },
    {'symbol': 'QQQ', 'exchange': 'NASDAQ', 'name': 'Invesco Tech', },
    {'symbol': 'VTV', 'exchange': 'NYSEARCA', 'name': 'Vanguard Value', },
]


def fetch(symbol):
    """Fetch securities data for a specific symbol/asset.

    Returns:
        quote (dict): a list of attributes for each asset

    """

    # load env variables, where API key is saved
    load_dotenv()

    url = 'https://finnhub.io/api/v1/quote'
    params = {
        'symbol': symbol,
        'token': os.getenv('FINNHUB_API_KEY'),
    }
    response = requests.get(url, params=params)
    quote = response.json()
    return quote


def collect(assets):
    """Fetch securities data for a COLLECTION of symbols/assets.

    Returns:
        assets (list): a list of assets with the dict of attributes for each

    Notes:
        Uses the "fetch" function, above to pull the data for each asset

    """

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
    """Sorts a list of assets

    Args:
        data (list): the list of assets produced by the "collect" function
        ord (str): the user's preferred sort order

    Returns:
        sorted_data (list): a list of assets, sorted

    """

    if (ord == 'percent_change'):
        reverse = True
    else:
        reverse = False
    sorted_data = sorted(data, key=lambda k: k[ord], reverse=reverse)
    return sorted_data
