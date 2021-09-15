
from datetime import datetime
from pprint import pprint
import json
import os
import requests
import pytz

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser


@login_required
def index(request):
    user_id = request.user.id
    page = 'weather'

    if user_id == 1:
        zip = 30360
    else:
        zip = 32344

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'zip': zip,
        'units': 'imperial',
        'appid': '78e85b0dbd4e78f3b0d172a58915c685'
    }
    response = requests.get(url, params=params)
    current = json.loads(response.text)

    forecast = None

    context = {
        'page': 'weather',
        'current': current,
        'forecast': forecast,
    }
    return render(request, 'weather/content.html', context)

