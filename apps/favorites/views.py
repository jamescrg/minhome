from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.favorites.forms import FavoriteForm
from apps.favorites.models import Favorite
from apps.folders.folders import select_folder
from apps.folders.models import Folder


@login_required
def index(request):
    """Display a list of folders and favorites

    Notes:
        Always displays folders.
        If a folder is selected, displays the favorites for a folder.

    """

    user = request.user

    folders = Folder.objects.filter(user=user, page="favorites").order_by("name")

    selected_folder = select_folder(request, "favorites")

    if selected_folder:
        favorites = Favorite.objects.filter(user=user, folder_id=selected_folder.id)
    else:
        favorites = Favorite.objects.filter(user=user, folder_id__isnull=True)

    favorites = favorites.order_by("name")

    context = {
        "page": "favorites",
        "edit": False,
        "folders": folders,
        "selected_folder": selected_folder,
        "favorites": favorites,
    }
    return render(request, "favorites/content.html", context)


@login_required
def add(request):
    """Add a new favorite

    Notes:
        GET: Display new favorite form
        POST: Add favorite to database

    """
    user = request.user
    folders = Folder.objects.filter(user=user, page="favorites").order_by("name")

    selected_folder = select_folder(request, "favorites")

    if request.method == "POST":
        form = FavoriteForm(request.POST)

        if form.is_valid():
            favorite = form.save(commit=False)
            favorite.user = user
            favorite.save()
            return redirect("favorites")

    else:
        if selected_folder:
            form = FavoriteForm(initial={"folder": selected_folder.id})
        else:
            form = FavoriteForm()

    form.fields["folder"].queryset = Folder.objects.filter(
        user=user, page="favorites"
    ).order_by("name")

    context = {
        "page": "favorites",
        "add": True,
        "action": "/favorites/add",
        "folders": folders,
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
    folders = Folder.objects.filter(user=user, page="favorites").order_by("name")

    selected_folder = select_folder(request, "favorites")

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

    form.fields["folder"].queryset = Folder.objects.filter(
        user=user, page="favorites"
    ).order_by("name")

    context = {
        "page": "favorites",
        "edit": True,
        "add": False,
        "action": f"/favorites/{id}/edit",
        "folders": folders,
        "selected_folder": selected_folder,
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
    return redirect("favorites")
