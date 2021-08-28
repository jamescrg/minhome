from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Folder

@login_required
def index(request):
    pass


def select(request, id, page):

    user_id = request.user.id

    if page != 'tasks':
        Folder.objects.filter(page=page, user_id=user_id).update(selected=0)
        if id > 0: 
            folder = get_object_or_404(Folder, pk=id)
            folder.selected = 1
            folder.save()
    
    if page == 'tasks':
        folder = get_object_or_404(Folder, pk=id)

        if folder.active == 1:
            folder.active = 0

        if folder.selected == 1:
            folder.selected = 0
        else:
            folder.selected = 1

        folder.save()

    return redirect(page)


def insert(request, page):
    folder = Folder()
    folder.user_id = request.user.id
    folder.page = page
    for field in folder.fillable:
         setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


def update(request, id, page):
    folder = get_object_or_404(Folder, pk=id)
    for field in folder.fillable:
         setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


def delete(request, id, page):
    folder = get_object_or_404(Folder, pk=id)
    folder.delete()
    return redirect(page)


def home(request, id, page):
    user_id = request.user.id
    folder = get_object_or_404(Folder, pk=id)

    if folder.home_column > 0: 
        folder.home_column = 0
        folder.home_rank = 0
    else: 
        folder.home_column = 4
        ranked_folders = Folder.objects.filter(user_id=user_id, 
                home_column=4).order_by('-home_rank')
        max_rank = ranked_folders[0].home_rank
        folder.home_rank = max_rank + 1

    folder.save()
    return redirect(page)
