
from datetime import datetime, date, time, timezone
from pprint import pprint
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

    # fetch current crypto data
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {
        'symbol': 'BTC,ETH,ADA,SOL,UNI,ALGO,MATIC,ATOM,XLM,FIL,XMR,NANO,SC',
        'convert': 'USD',
        'CMC_PRO_API_KEY': config.settings_local.CRYPTO_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        result = response.json()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        result = None

    # import app.helpers as helpers
    # return helpers.dump(result)

    context = {
        'page': 'crypto',
        'result': result,
    }
    return render(request, 'crypto/content.html', context)
