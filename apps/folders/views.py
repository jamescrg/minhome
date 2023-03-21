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

    user = request.user

    if page != "tasks":
        attr = f"{page}_folder"
        selected_folder_id = getattr(user, attr)
        if folder.id == selected_folder_id:
            setattr(user, attr, 0)
            user.save()

    if page == "tasks":
        attr = f"{page}_folders"
        selected_folder_ids = getattr(user, attr)
        if folder.id in selected_folder_id:
            selected_folder_ids.remove(folder.id)
            setattr(user, attr, selected_folder_ids)
            user.save()

    folder.delete()
    return redirect(page)


@login_required
def home(request, id, page):
    """Add a folder to the home page.

    Args:
        id (int): a Folder instance id
        page (str): the page to which function should redirect

    """

    user = request.user
    home_folder = get_object_or_404(Folder, pk=id)

    if not home_folder.home_column:

        destination_column = 5

        # sequence destination column
        # make sure the folders are sequential and adjacent
        folders = Folder.objects.filter(user=user, home_column=destination_column)
        folders = folders.order_by("home_rank")
        count = 1
        for folder in folders:
            folder.home_rank = count
            folder.save()
            count += 1

        # increment all up by one
        for folder in folders:
            folder.home_rank = folder.home_rank + 1
            folder.save()

        home_folder.home_column = destination_column
        home_folder.home_rank = 1

    else:

        home_folder.home_rank = 0
        home_folder.home_column = 0

    home_folder.save()
    return redirect(page)
