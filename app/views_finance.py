
from datetime import datetime, date, time, timezone
from pprint import pprint
from operator import itemgetter
import os
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
import config.settings_local


@login_required
def index(request):
    user_id = request.user.id

    positions = [
        {
            'symbol': 'GME',
            'exchange': 'NYSE',
            'name': 'Gamestop',
            'shares': 100,
            'cost_basis': 12000.00,
        },
        {
            'symbol': 'TSLA',
            'exchange': 'NASDAQ',
            'name': 'Tesla',
            'shares': 1,
            'cost_basis': 799.80,
        },
        {
            'symbol': 'TLRY',
            'exchange': 'NASDAQ',
            'name': 'Tilray',
            'shares': 50,
            'cost_basis': 1006.50,
        },
        {
            'symbol': 'SNDL',
            'exchange': 'NASDAQ',
            'name': 'Sundial',
            'shares': 100,
            'cost_basis': 610.00,
        },
    ]

    total_value = 0
    total_profit = 0
    total_cost = 0

    for position in positions:

        # fetch current crypto data
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'interval': '60min',
            'symbol': position['symbol'],
            'apikey': config.settings_local.ALPHAVANGAGE_STOCKS_API_KEY,
        }

        try:
            response = requests.get(url, params=params)
            result = response.json()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            import app.helpers as helpers
            return helpers.dump(e)

        hours = list(result.values())[1] # convert dict to list, take second value
        current = list(hours.values())[0]
        price = float(current['4. close'])

        position['price'] = price
        position['value'] = position['shares'] * price
        position['profit'] = position['value'] - position['cost_basis']
        position['return'] = position['profit'] / position['cost_basis'] * 100

        total_value += position['value']
        total_cost += position['cost_basis']
        total_profit += position['profit']
        total_return = total_profit / total_cost * 100

    positions = sorted(positions, key=lambda k: k['value'], reverse=True)

    context = {
        'page': 'finance',
        'positions': positions,
        'total_value': total_value,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'total_return': total_return,
    }
    return render(request, 'finance/content.html', context)
