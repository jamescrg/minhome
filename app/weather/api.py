#!/usr/bin/python3

import os
import requests

# fetch the api data
def get_response(url, params=None):
    response = requests.get(url, params=params)
    return response


# write the api data to a file
def write_response(response, file_name):
    os.chdir('/home/james/cp/app/weather')
    file = open(file_name, 'w')
    file.write(response.text)
    file.close()


if __name__=='__main__':

    # get current data
    # --------------------------

    # atlanta
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'zip': 30360,
        'units': 'imperial',
        'appid': '78e85b0dbd4e78f3b0d172a58915c685'
    }
    response = get_response(url, params)
    write_response(response, 'data_atlanta_current.json')

    # monticello
    params['zip'] = 32344
    response = get_response(url, params)
    write_response(response, 'data_monticello_current.json')

    # get seven day forecast
    # --------------------------

    # atlanta
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params = {
        'lat': 33.899990,
        'lon': -84.277679,
        'units': 'imperial',
        'exclude': 'current,hourly,minutely',
        'appid': '78e85b0dbd4e78f3b0d172a58915c685'
    }
    response = get_response(url, params)
    write_response(response, 'data_atlanta_forecast.json')

    # monticello
    params['lat'] = 30.543039
    params['lon'] = -83.862694
    response = get_response(url, params)
    write_response(response, 'data_monticello_forecast.json')
