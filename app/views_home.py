from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context = {
        'page': 'home',
    }

    return render(request, 'home/index.html', context)
