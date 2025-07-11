from django.db.models import Q
from django.shortcuts import get_object_or_404

from apps.folders.models import Folder


def get_task_folders(request, parent=None):
    user = request.user

    # get the task folders
    folders = Folder.objects.filter(page="tasks", parent=parent)

    # narrow down to the folders that are:
    # 1. owned by the user and
    # 2. edited by the user,
    # and then order the folders by name
    folders = folders.filter(Q(user=user) | Q(editors=user)).order_by("name")
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
    folders = folders.filter(Q(user=user) | Q(editors=user)).order_by("name")

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
        folders = Folder.objects.filter(pk__in=folder_path).select_related("parent")
        folder_dict = {f.id: f for f in folders}

        for folder_id in folder_path:
            if folder_id in folder_dict:
                breadcrumbs.append(folder_dict[folder_id])

    return breadcrumbs


def get_folder_tree(request, page, selected_folder=None, max_depth=5):
    """Get complete folder tree with hierarchical structure."""
    user = request.user

    def get_folder_children(parent_folder):
        """Get direct children of a folder."""
        return (
            Folder.objects.filter(page=page, parent=parent_folder)
            .filter(Q(user=user) | Q(editors=user))
            .order_by("name")
        )

    def build_tree_recursive(parent_folder, current_level=0):
        """Recursively build the folder tree."""
        children = get_folder_children(parent_folder)
        tree_nodes = []

        for folder in children:
            node = {
                "folder": folder,
                "level": current_level,
                "children": (
                    build_tree_recursive(folder, current_level + 1)
                    if current_level < max_depth
                    else []
                ),
                "has_children": get_folder_children(folder).exists(),
            }
            tree_nodes.append(node)

        return tree_nodes

    # Build the complete tree starting from root
    tree = build_tree_recursive(None, 0)

    # Check if any folder in the tree has children
    def has_any_children(nodes):
        for node in nodes:
            if node["has_children"]:
                return True
            if has_any_children(node["children"]):
                return True
        return False

    tree_has_children = has_any_children(tree)

    # Mark expansion state based on selected folder
    if selected_folder:
        ancestors = selected_folder.get_ancestors()
        ancestor_ids = [ancestor.id for ancestor in ancestors] + [selected_folder.id]

        def mark_expanded(nodes):
            for node in nodes:
                if node["folder"].id in ancestor_ids:
                    node["expanded"] = True
                    mark_expanded(node["children"])
                else:
                    node["expanded"] = False

        mark_expanded(tree)
    else:
        # If no folder is selected, mark all folders as collapsed by default
        def mark_collapsed(nodes):
            for node in nodes:
                node["expanded"] = False
                mark_collapsed(node["children"])

        mark_collapsed(tree)

    return tree, tree_has_children
