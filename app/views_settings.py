
from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context = {
        'page': 'settings',
    }

    return render(request, 'settings/index.html', context)
