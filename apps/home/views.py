import logging
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

import apps.home.google as google
from apps.favorites.models import Favorite
from apps.folders.models import Folder
from apps.home.toggle import show_section
from apps.tasks.models import Task

logger = logging.getLogger(__name__)


@login_required
def index(request):
    """Display the home page.

    Notes:
        Displays upcoming events, current tasks, and priority favorites

    """

    user = request.user
    session = request.session

    # EVENTS
    # ----------------

    # check whether events are shown are hidden
    show_events = show_section(session, "events")

    # if events are shown, load them
    if show_events:
        if user.google_credentials:
            events = google.get_events(user.id)
        else:
            events = None
    else:
        events = None

    # TASKS
    # ----------------

    # check whether tasks are shown or hidden
    show_tasks = show_section(session, "tasks")

    # if tasks are shown, check for task_folders
    task_folders = Folder.objects.filter(user=user, page="tasks", home_column__gt=1)
    if task_folders:
        for folder in task_folders:
            tasks = Task.objects.filter(folder_id=folder.id).exclude(status=1)
            tasks = tasks.order_by("status", "title")
            folder.tasks = tasks

    # check whether there are some tasks in any of the folders
    # if so, flag as true
    # the purpose of this flag is to show the tasks area
    # only if there are at least some unchecked tasks to display
    some_tasks = False
    if task_folders:
        for folder in task_folders:
            if folder.tasks:
                some_tasks = True

    # FAVORITES
    # ----------------

    columns = []
    for i in range(1, 5):
        folders = Folder.objects.filter(user=user, page="favorites", home_column=i)
        folders = folders.order_by("home_rank")
        for folder in folders:
            favorites = Favorite.objects.filter(folder_id=folder.id, home_rank__gt=0)
            favorites = favorites.order_by("home_rank")
            folder.favorites = favorites
        columns.append(folders)

    context = {
        "page": "home",
        "origin": "home",
        "search_engine": "google.com/search",
        "show_tasks": show_tasks,
        "task_folders": task_folders,
        "some_tasks": some_tasks,
        "events": events,
        "show_events": show_events,
        "columns": columns,
    }

    return render(request, "home/index.html", context)


@login_required
def toggle(request, section):
    """Toggle on or off various sections of the home page.

    Args:
        section (str): the section to toggle

    Notes:
        Page sections appear in the morning, this turns them off

        Session based, so that sections are only turned off for
        the specific browser from whcih they are toggled

    """

    allowed_sections = ["events", "tasks", "gathas"]

    if section in allowed_sections:
        # set the section name to use for the session key
        flag = "show_" + section
        exp = section + "_hide_expire"

        show_section = request.session.get(flag, True)

        if show_section:
            request.session[flag] = False
            request.session[exp] = date.today().strftime("%s")
        else:
            request.session[flag] = True

    return redirect("/home/")


@login_required
def folder(request, id, direction):
    """Move a folder up, down, left, or right

    Args:
        id (int): the folder to be moved
        direction (str): the direction in which to move the folder

    Notes:
        The home page has four columns. This function moves folders
        from one column to another, or up and down in an specific column.

    """

    user = request.user

    # if the stack order is being changed
    if direction == "up" or direction == "down":
        # get the folder to be moved
        # identify the column to which it belongs
        origin_folder = get_object_or_404(Folder, pk=id)
        origin_column = origin_folder.home_column

        # make sure the folders are sequential and adjacent
        folders = Folder.objects.filter(user=user, home_column=origin_column)
        folders = folders.order_by("home_rank")
        count = 1
        for folder in folders:
            folder.home_rank = count
            folder.save()
            count += 1

        # identify the origin rank as modified by the sequence operation
        origin_rank = origin_folder.home_rank

        # identify the destination rank
        if direction == "up":
            destination_rank = origin_rank - 1
        if direction == "down":
            destination_rank = origin_rank + 1

        # identify the folder to be displaced
        try:
            displaced_folder = Folder.objects.filter(
                user=user, home_column=origin_column, home_rank=destination_rank
            ).get()
        except Folder.DoesNotExist:
            displaced_folder = False

        # if a folder is being displaced, move it and the original folder
        if displaced_folder:
            origin_folder.home_rank = destination_rank
            origin_folder.save()
            displaced_folder.home_rank = origin_rank
            displaced_folder.save()

    # if the column is being changed
    if direction == "left" or direction == "right":
        # get the folder to be moved, along with its column and rank
        origin_folder = get_object_or_404(Folder, pk=id)
        origin_column = origin_folder.home_column

        if direction == "left" and origin_column > 1:
            destination_column = origin_column - 1
        elif direction == "right" and origin_column < 4:
            destination_column = origin_column + 1
        else:
            destination_column = origin_column

        # identify the bottom folder in the destination column
        # move over origin folder to destination column and place at bottom
        if destination_column != origin_column:
            bottom_folder = (
                Folder.objects.filter(user=user, home_column=destination_column)
                .order_by("-home_rank")
                .first()
            )
            bottom_rank = bottom_folder.home_rank
            origin_folder.home_column = destination_column
            origin_folder.home_rank = bottom_rank + 1

        # persist changes
        origin_folder.save()

        # resequence origin column
        # make sure the folders are sequential and adjacent
        folders = Folder.objects.filter(user=user, home_column=origin_column)
        folders = folders.order_by("home_rank")
        count = 1
        for folder in folders:
            folder.home_rank = count
            folder.save()
            count += 1

    return redirect("/home/")


@login_required
def favorite(request, id, direction):
    """Move a favorite up or down.

    Args:
        id (int): the favorite to be moved
        direction (str): the direction in which to move the favorite

    """

    user = request.user

    # get the favorite to be moved
    origin_favorite = get_object_or_404(Favorite, pk=id)
    folder_id = origin_favorite.folder_id

    # make sure the favorites are sequential and adjacent
    favorites = Favorite.objects.filter(user=user, folder_id=folder_id, home_rank__gt=0)
    favorites = favorites.order_by("home_rank")

    count = 1
    for favorite in favorites:
        favorite.home_rank = count
        favorite.save()
        count += 1

    favorites = Favorite.objects.filter(user=user, folder_id=folder_id, home_rank__gt=0)
    favorites = favorites.order_by("home_rank")

    # identify the origin rank as modified by the sequence operation
    origin_favorite = get_object_or_404(Favorite, pk=id)
    origin_rank = origin_favorite.home_rank

    # identify the destination rank
    if direction == "up":
        destination_rank = origin_rank - 1
    if direction == "down":
        destination_rank = origin_rank + 1

    # identify the favorite to be displaced
    displaced_favorite = Favorite.objects.filter(
        user=user, folder_id=folder_id, home_rank=destination_rank
    ).first()

    # if a favorite is being displaced, move it and the original favorite
    # otherwise, we are at the end of the column, make no changes

    # make sure the top favorite doesn't move if the user attempts to move it up
    if destination_rank > 0:
        origin_favorite.home_rank = destination_rank
        origin_favorite.save()

    if displaced_favorite:
        displaced_favorite.home_rank = origin_rank
        displaced_favorite.save()

    return redirect("/home/")
