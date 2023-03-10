from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from apps.folders.models import Folder


@login_required
def select(request, id, page):
    """Select a folder for display, redirect to index if that folder's page.

    Args:
        id (int): a Folder instance id
        page (int): the page to which the folder belongs

    """

    user = request.user

    if page != "tasks":
        setattr(user, page + "_folder", id)

    if page == "tasks":
        # if the folder is on the list, remove it
        if id in user.tasks_folders:
            user.tasks_folders.remove(id)

        # and deactivate it
            if user.tasks_active_folder == id:
                user.tasks_active_folder = 0

        # if the folder is not on the list, add it
        else:
            user.tasks_folders.append(id)

    user.save()

    return redirect(page)


@login_required
def insert(request, page):
    """Add a new folder.

    Args:
        page(str): the page to which the folder belongs

    Notes:
        Only accepts post requests

    """
    folder = Folder()
    folder.user = request.user
    folder.page = page
    for field in folder.fillable:
        setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


@login_required
def update(request, id, page):
    """Edit a folder.

    Args:
        id (str): a Folder instance id
        page (str): the page to which the folder belongs

    Notes:
        Only accepts post requests

    """

    try:
        folder = Folder.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")
    for field in folder.fillable:
        setattr(folder, field, request.POST.get(field))
    folder.save()
    return redirect(page)


@login_required
def delete(request, id, page):
    """Delete a folder

    Args:
        id (int): a Folder instance id
        page (str): the page to which the delete function should redirection

    """

    try:
        folder = Folder.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")
    folder.delete()
    if page != "tasks":
        if "selected_folders" in request.session:
            if page in request.session["selected_folders"]:
                del request.session["selected_folders"][page]
    if page == "tasks":
        if "selected_folders" in request.session:
            if "tasks" in request.session["selected_folders"]:
                if id in request.session["selected_folders"]["tasks"]:
                    request.session["selected_folders"]["tasks"].remove(id)
    return redirect(page)


# sets a folder to show on the home page
@login_required
def home(request, id, page):
    """Add a folder to the home page.

    Args:
        id (int): a Folder instance id
        page (str): the page to which function should redirect

    """

    user = request.user
    folder = get_object_or_404(Folder, pk=id)

    if folder.home_column:
        folder.home_column = 0
        folder.home_rank = 0
    else:
        folder.home_column = 4
        ranked_folders = Folder.objects.filter(user=user, home_column=4).order_by(
            "-home_rank"
        )
        if ranked_folders:
            max_rank = ranked_folders[0].home_rank
        else:
            max_rank = 0
        folder.home_rank = max_rank + 1

    folder.save()
    return redirect(page)
