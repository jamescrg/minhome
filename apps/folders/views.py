from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.folders.models import Folder
from accounts.models import CustomUser


@login_required
def select(request, id, page):
    """Select a folder for display, redirect to index if that folder's page.

    Args:
        id (int): a Folder instance id
        page (int): the page to which the folder belongs

    """
    user = request.user
    setattr(user, page + "_folder", id)
    user.save()
    
    # Store the current folder path for breadcrumbs
    if id and id != "0":
        try:
            folder = Folder.objects.get(pk=id)
            request.session[f"{page}_folder_path"] = [f.id for f in folder.get_ancestors()] + [folder.id]
        except Folder.DoesNotExist:
            request.session[f"{page}_folder_path"] = []
    else:
        request.session[f"{page}_folder_path"] = []
    
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
        value = request.POST.get(field)
        if field == 'parent' and value:
            # Convert parent ID to actual Folder instance
            try:
                value = Folder.objects.get(pk=value, user=request.user, page=page)
            except Folder.DoesNotExist:
                value = None
        setattr(folder, field, value)
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
        value = request.POST.get(field)
        if field == 'parent' and value:
            # Convert parent ID to actual Folder instance
            try:
                value = Folder.objects.get(pk=value, user=request.user, page=page)
                # Prevent setting a folder as its own parent or a descendant as parent
                if value.id == folder.id or folder in value.get_ancestors():
                    value = folder.parent  # Keep current parent
            except Folder.DoesNotExist:
                value = None
        setattr(folder, field, value)
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

    attr = f"{page}_folder"
    selected_folder_id = getattr(user, attr)
    if folder.id == selected_folder_id:
        setattr(user, attr, 0)
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
        folders = Folder.objects.filter(
            user=user, home_column=destination_column)
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


@login_required
def share(request, id, page):
    """Manage sharing for a folder.
    
    Args:
        id (int): a Folder instance id
        page (str): the page to which the folder belongs
    """
    try:
        folder = Folder.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")
    
    if request.method == 'POST':
        # Handle adding/removing users from sharing
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        if user_id and action:
            try:
                user = CustomUser.objects.get(pk=user_id)
                if action == 'add':
                    folder.editors.add(user)
                elif action == 'remove':
                    folder.editors.remove(user)
                return JsonResponse({'status': 'success'})
            except CustomUser.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'})
    
    # Get all users for sharing dropdown
    all_users = CustomUser.objects.exclude(pk=request.user.pk)
    current_editors = folder.editors.all()
    available_users = all_users.exclude(pk__in=current_editors.values_list('pk', flat=True))
    
    context = {
        'folder': folder,
        'page': page,
        'current_editors': current_editors,
        'available_users': available_users,
    }
    
    return render(request, 'folders/share.html', context)
