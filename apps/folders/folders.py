from django.shortcuts import get_object_or_404

from apps.folders.models import Folder
from accounts.models import CustomUser


def get_task_folders(request):
    user = request.user

    folders = Folder.objects.filter(user=user, page="tasks").order_by("name")

    # include my groceries lists in katie's folder list
    if user.username == 'katie':
        james_folders = Folder.objects.filter(id__in=[380, 354])
        folders = folders | james_folders
        folders.order_by("name")

    return folders


def select_folders(request, page):

    user = request.user

    if page == "tasks":
        folder_ids = user.tasks_folders

        if folder_ids:
            folders = Folder.objects.filter(pk__in=folder_ids).order_by("name")
        else:
            folders = []

        return folders

    else:

        folder_id = getattr(user, page + "_folder")

        if folder_id:
            folder = get_object_or_404(Folder, pk=folder_id)
        else:
            folder = None

        return folder
