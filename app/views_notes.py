from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def index(request):

    context = {
        'page': 'notes',
    }

    return render(request, 'notes/index.html', context)
