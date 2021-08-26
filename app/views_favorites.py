from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def index(request):

    user_id = request.user.id
    page = 'favorites'
    folders = Folder.objects.filter(user_id=user_id, page=page)

    context = {
        'page': 'favorites',
    }

    return render(request, 'favorites/index.html', context)
