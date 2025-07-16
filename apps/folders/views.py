import json
import logging

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from accounts.models import CustomUser
from apps.folders.folders import get_folder_tree, select_folder
from apps.folders.models import Folder

logger = logging.getLogger(__name__)


@login_required
def select(request, id, page, origin=None):
    """Select a folder for display, redirect to index if that folder's page.
    If the folder is already selected, unselect it.

    Args:
        id (int): a Folder instance id
        page (int): the page to which the folder belongs
        origin (str): optional origin page (e.g., 'home')

    """
    user = request.user
    current_folder_id = getattr(user, page + "_folder", None)

    # If clicking on the currently selected folder, unselect it
    # BUT not if coming from the home page - in that case always select
    if current_folder_id == id and origin != "home":
        setattr(user, page + "_folder", 0)
        user.save()
        request.session[f"{page}_folder_path"] = []
        return redirect(page)

    # Otherwise, select the new folder
    setattr(user, page + "_folder", id)
    user.save()

    # Store the current folder path for breadcrumbs
    if id and id != 0:
        try:
            folder = Folder.objects.get(pk=id)
            request.session[f"{page}_folder_path"] = [
                f.id for f in folder.get_ancestors()
            ] + [folder.id]

            # Also expand the selected folder
            session_key = f"{page}_expanded_folders"
            expanded_folders = set(request.session.get(session_key, []))
            expanded_folders.add(id)
            request.session[session_key] = list(expanded_folders)
            request.session.modified = True

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

    # For HTMX requests, always create folders at root level (no parent)
    if request.headers.get("HX-Request"):
        folder.parent = None
    else:
        # Always set parent to the currently selected folder
        selected_folder = select_folder(request, page)
        folder.parent = selected_folder

    for field in folder.fillable:
        value = request.POST.get(field)
        if field == "parent" and value:
            # Convert parent ID to actual Folder instance
            try:
                value = Folder.objects.get(pk=value, user=request.user, page=page)
            except Folder.DoesNotExist:
                value = None  # Root level for HTMX requests
        elif field == "parent":
            # If no parent specified, use None for HTMX requests
            value = (
                None
                if request.headers.get("HX-Request")
                else select_folder(request, page)
            )
        setattr(folder, field, value)
    folder.save()

    # Return partial update for HTMX requests
    if request.headers.get("HX-Request"):
        from django.shortcuts import render

        selected_folder = select_folder(request, page)
        folder_tree, tree_has_children = get_folder_tree(request, page, selected_folder)
        return render(
            request,
            "folders/list_fragment.html",
            {
                "folder_tree": folder_tree,
                "tree_has_children": tree_has_children,
                "selected_folder": selected_folder,
                "page": page,
            },
        )

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
        if field == "parent":
            # Skip parent field - keep folder in the same parent
            continue
        value = request.POST.get(field)
        setattr(folder, field, value)
    folder.save()

    # Return partial update for HTMX requests
    if request.headers.get("HX-Request"):
        from django.shortcuts import render

        selected_folder = select_folder(request, page)
        folder_tree, tree_has_children = get_folder_tree(request, page, selected_folder)
        return render(
            request,
            "folders/list_fragment.html",
            {
                "folder_tree": folder_tree,
                "tree_has_children": tree_has_children,
                "selected_folder": selected_folder,
                "page": page,
            },
        )

    return redirect(page)


@login_required
def edit_form(request, id, page):
    """Return the edit form for a folder (for HTMX modal)."""
    try:
        folder = Folder.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")

    return render(request, "folders/edit_modal.html", {"folder": folder, "page": page})


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

    if request.method == "POST":
        # Handle adding/removing users from sharing
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")

        if user_id and action:
            try:
                user = CustomUser.objects.get(pk=user_id)
                if action == "add":
                    folder.editors.add(user)
                elif action == "remove":
                    folder.editors.remove(user)
                return JsonResponse({"status": "success"})
            except CustomUser.DoesNotExist:
                return JsonResponse({"status": "error", "message": "User not found"})

    # Get all users for sharing dropdown
    all_users = CustomUser.objects.exclude(pk=request.user.pk)
    current_editors = folder.editors.all()
    available_users = all_users.exclude(
        pk__in=current_editors.values_list("pk", flat=True)
    )

    context = {
        "folder": folder,
        "page": page,
        "current_editors": current_editors,
        "available_users": available_users,
    }

    return render(request, "folders/share.html", context)


@login_required
@csrf_exempt
def move(request, id, page):
    """Move a folder to a new parent.

    Args:
        id (int): The folder ID to move
        page (str): The page type (favorites, contacts, notes, tasks)

    Returns:
        JsonResponse with success/error status
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST request required"})

    try:
        # Get the folder to move
        folder = Folder.objects.get(pk=id, user=request.user, page=page)

        # Store old inherited editors for permission cleanup
        old_inherited_editors = folder.get_inherited_editors()

        # Parse the request body
        data = json.loads(request.body)
        new_parent_id = data.get("new_parent_id")

        # Get the new parent folder
        if new_parent_id:
            try:
                new_parent = Folder.objects.get(
                    pk=new_parent_id, user=request.user, page=page
                )

                # Prevent moving a folder into one of its descendants
                if folder in new_parent.get_ancestors() or folder.id == new_parent.id:
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "Cannot move folder into its descendant or itself",
                        }
                    )

                # Check depth limit (3 levels maximum)
                new_parent_depth = len(new_parent.get_ancestors())
                if (
                    new_parent_depth >= 2
                ):  # 0-indexed: 0=root, 1=level1, 2=level2 (can't add level3)
                    return JsonResponse(
                        {
                            "success": False,
                            "error": "Cannot nest folders more than 3 levels deep",
                        }
                    )

                folder.parent = new_parent
            except Folder.DoesNotExist:
                return JsonResponse(
                    {"success": False, "error": "Target folder not found"}
                )
        else:
            # Move to root level
            folder.parent = None

        folder.save()

        # Apply permission inheritance changes after parent is set
        new_inherited_editors = folder.get_inherited_editors()

        # Remove old inherited permissions that are no longer valid
        editors_to_remove = old_inherited_editors - new_inherited_editors
        if editors_to_remove:
            # Remove from folder and all its descendants
            for editor in editors_to_remove:
                folder.editors.remove(editor)
            folder.remove_inherited_permissions_from_descendants(editors_to_remove)

        # Add new inherited permissions
        editors_to_add = new_inherited_editors - old_inherited_editors
        if editors_to_add:
            # Add to folder and all its descendants
            for editor in editors_to_add:
                folder.editors.add(editor)
            folder.propagate_permissions_to_descendants()

        return JsonResponse({"success": True})

    except Folder.DoesNotExist:
        return JsonResponse({"success": False, "error": "Folder not found"})
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON data"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def toggle_folder(request, id, page):
    """Toggle the expand/collapse state of a folder."""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST request required"})

    session_key = f"{page}_expanded_folders"
    expanded_folders = set(request.session.get(session_key, []))

    folder_id = int(id)
    if folder_id in expanded_folders:
        expanded_folders.remove(folder_id)
        is_expanded = False
    else:
        expanded_folders.add(folder_id)
        is_expanded = True

    request.session[session_key] = list(expanded_folders)
    request.session.modified = True

    return JsonResponse({"success": True, "is_expanded": is_expanded})


@login_required
def collapse_all_folders(request, page):
    """Collapse all folders by clearing the expanded folders from session."""
    # Clear expanded folders from session
    session_key = f"{page}_expanded_folders"
    request.session[session_key] = []
    request.session.modified = True

    # Return the updated folder list for HTMX
    selected_folder = select_folder(request, page)
    folder_tree, tree_has_children = get_folder_tree(request, page, selected_folder)

    return render(
        request,
        "folders/list_fragment.html",
        {
            "folder_tree": folder_tree,
            "tree_has_children": tree_has_children,
            "selected_folder": selected_folder,
            "page": page,
        },
    )
