
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

    pwd = os.path.dirname(__file__)
    file = open(pwd + '/data_current.json', 'r')
    current = json.loads(file.read())

    context = {
        'page': 'weather',
        'current': current,
    }
    return render(request, 'weather/content.html', context)

