
from django.shortcuts import get_object_or_404

from apps.folders.models import Folder


def selected_folders(request, page):

    selected_folder_id = request.session.get('selected_folders', {}).get(page, None)

    if selected_folder_id:
        selected_folder = get_object_or_404(Folder, pk=selected_folder_id)
    else:
        selected_folder = None

    return selected_folder
