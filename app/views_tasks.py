
from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context = {
        'page': 'tasks',
    }

    return render(request, 'tasks/index.html', context)
