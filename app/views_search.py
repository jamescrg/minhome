
from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context = {
        'page': 'search',
    }

    return render(request, 'search/index.html', context)
