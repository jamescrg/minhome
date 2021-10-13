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
import config.settings_local
from config.helpers import timestamp_to_eastern


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
        'appid': config.settings_local.OPEN_WEATHER_API_KEY,
    }

    response = requests.get(url, params=params)
    current = response.json()

    # convert sunrise to Eastern time and readable string format
    sunrise = timestamp_to_eastern(current['sys']['sunrise'])
    current['sunrise'] = sunrise.strftime("%I:%M %p")

    # convert sunset to Eastern time and readable string format
    sunset = timestamp_to_eastern(current['sys']['sunset'])
    current['sunset'] = sunset.strftime("%I:%M %p")

    # fetch forecast data
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params['lon'] = current['coord']['lon']
    params['lat'] = current['coord']['lat']
    params['exclude'] = 'minutely'
    del params['zip']
    response = requests.get(url, params=params)
    forecast = response.json()

    forecast['daily'] = forecast['daily'][1:]
    forecast['hourly'] = forecast['hourly'][1:13]
    
    for hour in forecast['hourly']:
        # convert hour to Eastern time and readable string format
        hour_time = timestamp_to_eastern(hour['dt'])
        hour['hour_time'] = hour_time.strftime("%I:%M %p")

    for day in forecast['daily']:
        date = datetime.fromtimestamp(day['dt'])
        day['date_string'] = date.strftime("%A")

    context = {
        'page': 'weather',
        'current': current,
        'forecast': forecast,
    }
    return render(request, 'weather/content.html', context)
