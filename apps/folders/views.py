

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from apps.folders.models import Folder


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
    try:
        folder = Folder.objects.filter(user_id=request.user.id, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404('Record not found.')
    for field in folder.fillable:
        setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


def delete(request, id, page):
    try:
        folder = Folder.objects.filter(user_id=request.user.id, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404('Record not found.')
    folder.delete()
    return redirect(page)


# sets a folder to show on the home page
def home(request, id, page):
    user_id = request.user.id
    folder = get_object_or_404(Folder, pk=id)

    if folder.home_column:
        folder.home_column = 0
        folder.home_rank = 0
    else:
        folder.home_column = 4
        ranked_folders = Folder.objects.filter(user_id=user_id, home_column=4).order_by(
            '-home_rank'
        )
        if ranked_folders:
            max_rank = ranked_folders[0].home_rank
        else:
            max_rank = 0
        folder.home_rank = max_rank + 1

    folder.save()
    return redirect(page)
