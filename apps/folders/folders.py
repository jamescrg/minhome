
from django.shortcuts import get_object_or_404

from apps.folders.models import Folder


def select_folders(request, page):

    if page == 'tasks':

        selected_folder_ids = request.session.get('selected_folders', {}).get(page, None)

        if selected_folder_ids:
            selected_folders = Folder.objects.filter(pk__in=selected_folder_ids)
        else:
            selected_folders = []

        return selected_folders

    else:

        selected_folder_id = request.session.get('selected_folders', {}).get(page, None)

        if selected_folder_id:
            selected_folder = get_object_or_404(Folder, pk=selected_folder_id)
        else:
            selected_folder = None

        return selected_folder
