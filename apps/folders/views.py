

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from apps.folders.models import Folder


@login_required
def select(request, id, page):

    if not request.session.get('selected_folders'):
        request.session['selected_folders'] = {}

    if page != 'tasks':
        request.session['selected_folders'][page] = id

    if page == 'tasks':

        # if there are no active task folders, initialize a list
        if not request.session['selected_folders'].get('tasks'):
            request.session['selected_folders']['tasks'] = []

        # if the folder is on the list, remove it
        if id in request.session['selected_folders']['tasks']:
            request.session['selected_folders']['tasks'].remove(id)

        # if the folder is not on the list, add it
        else:
            request.session['selected_folders']['tasks'].append(id)

        # if the folder is active, deactivate it
        if request.session.get('active_task_folder'):
            if request.session.get('active_task_folder') == id:
                del request.session['active_task_folder']

    return redirect(page)


@login_required
def insert(request, page):
    folder = Folder()
    folder.user_id = request.user.id
    folder.page = page
    for field in folder.fillable:
        setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


@login_required
def update(request, id, page):
    try:
        folder = Folder.objects.filter(user_id=request.user.id, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404('Record not found.')
    for field in folder.fillable:
        setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


@login_required
def delete(request, id, page):
    try:
        folder = Folder.objects.filter(user_id=request.user.id, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404('Record not found.')
    folder.delete()
    return redirect(page)


# sets a folder to show on the home page
@login_required
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
