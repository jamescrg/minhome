
from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.weather.timeshift import timestamp_to_eastern

from config import settings_local


@login_required
def index(request):
    """Display current weather conditions at a specified zip code.

    TODO:
        * Create a user's zip code attribute and store the zip code there.
        * Have the user register a zip code up on creating
        * Allow the user the change their zip code through the settings page.
    """

    if request.user.id == 1:
        zip = 30360
    else:
        zip = 30533


    # fetch current weather data
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'zip': zip,
        'units': 'imperial',
        'appid': settings_local.OPEN_WEATHER_API_KEY,
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
