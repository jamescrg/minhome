from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def index(request):

    context = {
        'page': 'settings',
    }

    return render(request, 'settings/index.html', context)
