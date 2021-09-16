
from datetime import datetime, date, time, timezone
from pprint import pprint
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

    # fetch current weather data
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'zip': zip,
        'units': 'imperial',
        'appid': '78e85b0dbd4e78f3b0d172a58915c685'
    }
    response = requests.get(url, params=params)
    current = response.json()

    # convert sunrise to Eastern time and readable string format
    sunrise = datetime.fromtimestamp(current['sys']['sunrise'])
    sunrise = sunrise.replace(tzinfo=timezone.utc)
    tz = pytz.timezone('US/Eastern')
    sunrise = sunrise.astimezone(tz)
    current['sunrise'] = sunrise.strftime("%I:%M %p")

    # convert sunset to Eastern time and readable string format
    sunset = datetime.fromtimestamp(current['sys']['sunset'])
    sunset = sunset.replace(tzinfo=timezone.utc)
    tz = pytz.timezone('US/Eastern')
    sunset = sunset.astimezone(tz)
    current['sunset'] = sunset.strftime("%I:%M %p")

    # fetch forecast data
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params['lon'] = current['coord']['lon']
    params['lat'] = current['coord']['lat']
    params['exclude'] = 'minutely,hourly'
    del params['zip']
    response = requests.get(url, params=params)
    forecast = response.json()

    for day in forecast['daily']:
        date = datetime.fromtimestamp(day['dt'])
        day['date_string'] = date.strftime("%A")

    context = {
        'page': 'weather',
        'current': current,
        'forecast': forecast,
    }
    return render(request, 'weather/content.html', context)

