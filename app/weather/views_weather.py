
from datetime import datetime
from pprint import pprint
import json
import os
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
        city = 'atlanta'
    else:
        city = 'monticello'

    pwd = os.path.dirname(__file__)

    file = open(f'{pwd}/data_{city}_current.json', 'r')
    current = file.read()
    file.close()
    current = json.loads(current)

    file = open(f'{pwd}/data_{city}_forecast.json', 'r')
    forecast = file.read()
    file.close()
    forecast = json.loads(forecast)

    # import app.util as util
    # return util.dump(current)

    context = {
        'page': 'weather',
        'current': current,
        'forecast': forecast,
    }
    return render(request, 'weather/content.html', context)

