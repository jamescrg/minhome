from datetime import datetime

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.weather.timeshift import timestamp_to_eastern


@login_required
def index(request):
    """Display current weather conditions at a specified zip code."""

    # get zip code
    user = request.user
    zip = user.zip
    zip_valid = True

    # if zip code is a nonzero value, fetch data
    if zip:

        # fetch current weather data
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "zip": zip,
            "units": "imperial",
            "appid": settings.OPEN_WEATHER_API_KEY,
        }
        response = requests.get(url, params=params)
        current = response.json()

        # check for an invalid zip code
        if "message" in current:
            zip_valid = False

        # if the zip code is valid, proceed with loading data
        if zip_valid:

            # convert sunrise to Eastern time and readable string format
            sunrise = timestamp_to_eastern(current["sys"]["sunrise"])
            current["sunrise"] = sunrise.strftime("%I:%M %p")

            # convert sunset to Eastern time and readable string format
            sunset = timestamp_to_eastern(current["sys"]["sunset"])
            current["sunset"] = sunset.strftime("%I:%M %p")

            # fetch forecast data
            url = "https://api.openweathermap.org/data/3.0/onecall"
            params["lon"] = current["coord"]["lon"]
            params["lat"] = current["coord"]["lat"]
            params["exclude"] = "minutely"
            del params["zip"]
            response = requests.get(url, params=params)
            forecast = response.json()

            forecast["daily"] = forecast["daily"][1:]
            forecast["hourly"] = forecast["hourly"][1:13]

            for hour in forecast["hourly"]:
                # convert hour to Eastern time and readable string format
                hour_time = timestamp_to_eastern(hour["dt"])
                hour["hour_time"] = hour_time.strftime("%I:%M")

            for day in forecast["daily"]:
                date = datetime.fromtimestamp(day["dt"])
                day["date_string"] = date.strftime("%A")

            context = {
                "page": "weather",
                "current": current,
                "forecast": forecast,
            }
            return render(request, "weather/content.html", context)

        else:

            # if zip code is invalid, load start page with status
            # of invalid zip code
            context = {
                "page": "weather",
                "status": "invalid zip",
                "current": None,
                "forecast": None,
            }
            return render(request, "weather/content.html", context)

    else:

        # if zip code is invalid, load start page with status
        # of empty zip code
        context = {
            "page": "weather",
            "status": "no zip",
            "current": None,
            "forecast": None,
        }
        return render(request, "weather/content.html", context)


@login_required
def zip(request):
    """Sets the user's zip code."""
    user = request.user
    user.zip = request.POST["zip"]
    user.save()
    return redirect("/weather")
