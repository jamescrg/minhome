from apps.favorites.models import Favorite
from apps.folders.folders import get_breadcrumbs, get_folder_tree, select_folder


def get_favorites(request):
    """Display a list of folders and favorites

    Notes:
        Always displays folders.
        If a folder is selected, displays the favorites for a folder.

    """

    user = request.user

    selected_folder = select_folder(request, "favorites")

    # Update folder path in session for breadcrumbs if folder is selected
    if selected_folder:
        request.session["favorites_folder_path"] = [
            f.id for f in selected_folder.get_ancestors()
        ] + [selected_folder.id]
    else:
        request.session["favorites_folder_path"] = []

    # Get folder tree starting from selected folder
    folder_tree, tree_has_children = get_folder_tree(
        request, "favorites", selected_folder
    )

    # Get breadcrumbs for navigation
    breadcrumbs = get_breadcrumbs(request, "favorites")

    if selected_folder:
        # Get favorites from selected folder only
        favorites = Favorite.objects.filter(user=user, folder=selected_folder)
    else:
        favorites = Favorite.objects.filter(user=user, folder_id__isnull=True)

    favorites = favorites.order_by("name")

    context = {
        "page": "favorites",
        "edit": False,
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
        "selected_folder": selected_folder,
        "favorites": favorites,
        "breadcrumbs": breadcrumbs,
    }

    return context
