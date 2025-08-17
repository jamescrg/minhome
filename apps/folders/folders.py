from django.db.models import Q

from apps.folders.models import Folder


def get_task_folders(request):
    user = request.user

    # get the task folders
    folders = Folder.objects.filter(page="tasks")

    # narrow down to the folders that are:
    # 1. owned by the user and
    # 2. edited by the user,
    # and then order the folders by name
    folders = folders.filter(Q(user=user) | Q(editors=user)).order_by("name")
    return folders


def get_folders_for_page(request, page):
    """Get folders for a specific page that the user owns or has edit access to."""
    user = request.user

    folders = Folder.objects.filter(page=page)

    # Get folders that are owned by the user or shared with them
    folders = folders.filter(Q(user=user) | Q(editors=user)).order_by("name")

    return folders


def select_folder(request, page):

    user = request.user

    folder_id = getattr(user, page + "_folder")

    if folder_id and folder_id > 0:
        try:
            # Check if folder exists and user has access to it
            folder = Folder.objects.filter(
                Q(user=user) | Q(editors=user), pk=folder_id
            ).first()

            if not folder:
                # Folder doesn't exist or user doesn't have access
                # Clear the invalid folder reference
                setattr(user, page + "_folder", 0)
                user.save()
                folder = None
        except Exception:
            # Clear the invalid folder reference on any error
            setattr(user, page + "_folder", 0)
            user.save()
            folder = None
    else:
        folder = None

    return folder
