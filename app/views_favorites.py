
from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context = {
        'page': 'favorites',
    }

    return render(request, 'favorites/index.html', context)
