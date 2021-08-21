
from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context = {
        'page': 'contacts',
    }

    return render(request, 'contacts/index.html', context)
