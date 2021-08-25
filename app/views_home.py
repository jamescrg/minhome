from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import app.util as util
from pprint import pprint
from django.http import HttpResponse

from .models import Folder, Favorite

# @login_required
def index(request):

    columns = []
    for i in range(1, 5):
        folders = Folder.objects.filter(user_id = 1, home_column = i)
        folders = folders.order_by('home_rank')
        for folder in folders:
            favorites = Favorite.objects.filter(folder_id = folder.id, home_rank__gt = 0)
            folder.favorites = favorites
        columns.append(folders)

    context = {
        'page': 'home',
        'columns': columns,
    }

    return render(request, 'home/index.html', context)
    


# @login_required
def test(request):
    
    folders = Folder.objects.filter(user_id__gt=1)
    folders = folders.order_by('home_rank')

    folder = Folder.objects.get(pk=117)

    test_dict = {
        'page': 'home',
        'test': 'home',
        'this': 'home',
        'that': 'home',
    }

    test_var = 1.5

    return util.dump(folders)

    return HttpResponse('Hello World, this was a test')

