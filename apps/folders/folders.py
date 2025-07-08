from django.shortcuts import get_object_or_404
from django.db.models import Q

from apps.folders.models import Folder
from accounts.models import CustomUser


def get_task_folders(request, parent=None):
    user = request.user

    # get the task folders
    folders = Folder.objects.filter(page="tasks", parent=parent)

    # narrow down to the folders that are:
    # 1. owned by the user and
    # 2. edited by the user,
    # and then order the folders by name
    folders = folders.filter(
        Q(user=user)
        | Q(editors=user)
    ).order_by("name")
    return folders


def get_folders_for_page(request, page, parent=None):
    """Get folders for a specific page that the user owns or has edit access to.
    
    Args:
        request: The HTTP request object
        page: The page type (e.g., 'tasks', 'notes', etc.)
        parent: Optional parent folder to filter by (None for root folders)
    """
    user = request.user
    
    folders = Folder.objects.filter(page=page, parent=parent)
    
    # Get folders that are owned by the user or shared with them
    folders = folders.filter(
        Q(user=user)
        | Q(editors=user)
    ).order_by("name")
    
    return folders


def select_folder(request, page):
    user = request.user
    folder_id = getattr(user, page + "_folder")

    if folder_id:
        folder = get_object_or_404(Folder, pk=folder_id)
    else:
        folder = None

    return folder


def get_breadcrumbs(request, page):
    """Get breadcrumb navigation for the current folder."""
    folder_path = request.session.get(f"{page}_folder_path", [])
    breadcrumbs = []
    
    if folder_path:
        folders = Folder.objects.filter(pk__in=folder_path).select_related('parent')
        folder_dict = {f.id: f for f in folders}
        
        for folder_id in folder_path:
            if folder_id in folder_dict:
                breadcrumbs.append(folder_dict[folder_id])
    
    return breadcrumbs
