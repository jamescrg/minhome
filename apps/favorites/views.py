import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.favorites.favorites import get_favorites
from apps.favorites.forms import FavoriteExtensionForm, FavoriteForm
from apps.favorites.models import Favorite
from apps.folders.folders import get_folder_tree, get_folders_for_page, select_folder
from apps.folders.models import Folder


def cors_headers(view_func):
    """Decorator to add CORS headers for extension requests"""

    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-CSRFToken"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    return wrapper


@login_required
def index(request):
    context = get_favorites(request)
    return render(request, "favorites/content.html", context)


@login_required
def add(request):
    """Add a new favorite

    Notes:
        GET: Display new favorite form
        POST: Add favorite to database

    """
    user = request.user
    selected_folder = select_folder(request, "favorites")

    folder_tree, tree_has_children = get_folder_tree(
        request, "favorites", selected_folder
    )

    if request.method == "POST":
        form = FavoriteForm(request.POST)

        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = user
            favorite.folder = selected_folder  # Always assign to selected folder
            favorite.save()
            return redirect("favorites")

    else:
        # Pre-fill form with URL parameters if provided (for bookmarklet)
        initial_data = {}

        # Check for extension parameters
        name = request.GET.get("name", "").strip()
        url = request.GET.get("url", "").strip()
        if name:
            initial_data["name"] = name
        if url:
            initial_data["url"] = url

        form = FavoriteForm(initial=initial_data)

    context = {
        "page": "favorites",
        "add": True,
        "action": "/favorites/add",
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
        "selected_folder": selected_folder,
        "form": form,
    }

    return render(request, "favorites/content.html", context)


@login_required
def edit(request, id):
    """Edit a favorite
    Args:
        id (int): a Favorite instance id

    GET: Display favorite form
    POST: Update favorite in database

    """
    user = request.user
    selected_folder = select_folder(request, "favorites")

    folder_tree, tree_has_children = get_folder_tree(request, "notes", selected_folder)

    favorite = get_object_or_404(Favorite, pk=id)

    if request.method == "POST":
        try:
            favorite = get_object_or_404(Favorite, pk=id)
        except ObjectDoesNotExist:
            raise Http404("Record note found.")

        form = FavoriteForm(request.POST, instance=favorite)

        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = user
            favorite.save()
            return redirect("favorites")

    else:
        if selected_folder:
            form = FavoriteForm(
                instance=favorite, initial={"folder": selected_folder.id}
            )
        else:
            form = FavoriteForm(instance=favorite)

    context = {
        "page": "favorites",
        "edit": True,
        "add": False,
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
        "selected_folder": selected_folder,
        "action": f"/favorites/{id}/edit",
        "form": form,
    }

    return render(request, "favorites/content.html", context)


@login_required
def delete(request, id):
    """
    Delete a favorite

    Args:
        id (int): a Favorite instance id

    """
    try:
        favorite = Favorite.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")
    favorite.delete()
    return redirect("favorites")


@login_required
def home(request, id):
    """Add or remove a favorite from home

    Args:
        id (int): a Favorite instance id

    """
    favorite = get_object_or_404(Favorite, pk=id)
    if favorite.home_rank:
        favorite.home_rank = 0
    else:
        favorite.home_rank = 1
    favorite.save()
    context = get_favorites(request)
    return render(request, "favorites/favorites_list.html", context)


@cors_headers
@csrf_exempt
def api_add(request):
    """API endpoint to add a favorite via extension

    Expected POST data:
        name: The name/title of the favorite
        url: The URL to save
        folder_id: (optional) ID of folder to save to
    """
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        return JsonResponse({})

    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Authentication required"})

    try:
        name = request.POST.get("name", "").strip()
        url = request.POST.get("url", "").strip()
        folder_id = request.POST.get("folder_id", "").strip()

        # Validate required fields
        if not name or len(name) < 2:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Name is required and must be at least 2 characters",
                }
            )

        if len(name) > 100:
            return JsonResponse(
                {"success": False, "error": "Name must be 100 characters or less"}
            )

        if url and len(url) > 255:
            return JsonResponse(
                {"success": False, "error": "URL must be 255 characters or less"}
            )

        # Create the favorite
        favorite = Favorite(user=request.user, name=name, url=url)

        # Set folder if provided
        if folder_id:
            try:
                folder_id = int(folder_id)
                folder = Folder.objects.get(pk=folder_id, user=request.user)
                favorite.folder = folder
            except (ValueError, Folder.DoesNotExist):
                return JsonResponse({"success": False, "error": "Invalid folder ID"})

        # Set home_rank to 1 to make it visible on home page
        favorite.home_rank = 1
        favorite.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Favorite added successfully",
                "favorite": {
                    "id": favorite.id,
                    "name": favorite.name,
                    "url": favorite.url,
                    "folder_id": favorite.folder_id if favorite.folder else None,
                },
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@cors_headers
@csrf_exempt
def api_folders(request):
    """API endpoint to get user's folders for extension"""
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        return JsonResponse({})

    if request.method != "GET":
        return JsonResponse({"success": False, "error": "Only GET method allowed"})

    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "error": "Authentication required"})

    try:
        folders = get_folders_for_page(request, "favorites")
        folder_list = [{"id": folder.id, "name": folder.name} for folder in folders]

        return JsonResponse({"success": True, "folders": folder_list})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def extension_add(request):

    if request.method == "POST":
        form = FavoriteExtensionForm(request.POST)
        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = request.user
            favorite.home_rank = 1  # Show on home page
            favorite.save()
            # Return a simple success page
            return render(
                request, "favorites/extension_success.html", {"favorite": favorite}
            )
        # If form is not valid, it will fall through and re-render with errors
    else:
        # Pre-fill form with URL parameters
        initial_data = {}
        name = request.GET.get("name", "").strip()
        url = request.GET.get("url", "").strip()
        if name:
            initial_data["name"] = name
        if url:
            initial_data["url"] = url

        form = FavoriteExtensionForm(initial=initial_data)
        form.fields["folder"].queryset = Folder.objects.filter(
            page="favorites", user=request.user, parent=None
        ).order_by("name")

    context = {
        "form": form,
        "page_title": "Add Favorite",
        "name": request.GET.get("name", ""),
        "url": request.GET.get("url", ""),
    }
    return render(request, "favorites/extension_form.html", context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def move_to_folder(request):
    """Move a favorite to a different folder.

    Expected POST data:
        item_id: ID of the favorite to move
        folder_id: ID of the target folder
    """
    try:
        data = json.loads(request.body)
        item_id = data.get("item_id")
        folder_id = data.get("folder_id")

        if not item_id or not folder_id:
            return JsonResponse(
                {"success": False, "message": "Missing required parameters"}
            )

        # Get the favorite
        favorite = get_object_or_404(Favorite, pk=item_id, user=request.user)

        # Get the target folder
        folder = get_object_or_404(Folder, pk=folder_id, user=request.user)

        # Move the favorite to the new folder
        favorite.folder = folder
        favorite.save()

        return JsonResponse({"success": True, "message": "Favorite moved successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON data"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
