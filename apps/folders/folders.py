from django.db.models import Q

from apps.folders.models import Folder, UserFolderPosition


def get_accessible_folder_ids(user, page):
    """Get IDs of all folders a user can access, including descendants of shared folders.

    Args:
        user: The user to check access for
        page: The page type (tasks, notes, contacts, favorites)

    Returns:
        set: Set of folder IDs the user can access
    """
    # Direct access: owned or explicitly shared
    direct_access = Folder.objects.filter(page=page).filter(
        Q(user=user) | Q(editors=user)
    )

    all_accessible_ids = set(direct_access.values_list("id", flat=True))

    # For shared folders, also include their descendants
    shared_folders = Folder.objects.filter(page=page, editors=user)

    for folder in shared_folders:
        for descendant in folder.get_descendants():
            all_accessible_ids.add(descendant.id)

    return all_accessible_ids


def get_folders_for_page(request, page):
    """Get all accessible folders for a specific page.

    Args:
        request: The HTTP request object
        page: The page type (tasks, notes, contacts, favorites)

    Returns:
        QuerySet: Folders the user can access, ordered by name
    """
    user = request.user
    accessible_ids = get_accessible_folder_ids(user, page)

    folders = (
        Folder.objects.filter(id__in=accessible_ids)
        .select_related("parent")
        .prefetch_related("children", "editors")
        .order_by("name")
    )

    return folders


def get_folders_tree(request, page):
    """Get folders organized as a tree structure for sidebar display.

    Args:
        request: The HTTP request object
        page: The page type (tasks, notes, contacts, favorites)

    Returns:
        list: Tree structure where each node is {'folder': Folder, 'children': [...]}
    """
    user = request.user
    folders = get_folders_for_page(request, page)

    # Get user's folder positions for shared folders
    user_positions = {
        pos.folder_id: pos.local_parent_id
        for pos in UserFolderPosition.objects.filter(user=user, folder__page=page)
    }

    # Build lookup dict
    folder_dict = {f.id: f for f in folders}

    # Determine effective parent for each folder
    def get_effective_parent_id(folder):
        """Get the effective parent ID, considering user positions for shared folders."""
        if folder.user == user:
            # User owns this folder - use actual parent
            return folder.parent_id
        else:
            # Shared folder - check for user position
            if folder.id in user_positions:
                return user_positions[folder.id]
            # Default to root level for shared folders without position
            return None

    # Build tree
    root_folders = []
    for folder in folders:
        effective_parent_id = get_effective_parent_id(folder)
        if effective_parent_id is None or effective_parent_id not in folder_dict:
            root_folders.append(folder)

    def build_tree(folder):
        """Recursively build tree with children."""
        children = []
        for f in folders:
            if get_effective_parent_id(f) == folder.id:
                children.append(f)
        children.sort(key=lambda x: x.name.lower())
        return {"folder": folder, "children": [build_tree(child) for child in children]}

    root_folders.sort(key=lambda x: x.name.lower())
    return [build_tree(f) for f in root_folders]


def get_folders_flat_indented(request, page):
    """Get folders as flat list with indentation info for form dropdowns.

    Args:
        request: The HTTP request object
        page: The page type (tasks, notes, contacts, favorites)

    Returns:
        list: Flat list of dicts with 'folder', 'level', 'indent' keys
    """
    tree = get_folders_tree(request, page)
    flat_list = []

    def flatten(node, level=0):
        flat_list.append(
            {
                "folder": node["folder"],
                "level": level,
                "indent": "\u00a0\u00a0\u00a0\u00a0" * level,  # Non-breaking spaces
            }
        )
        for child in node["children"]:
            flatten(child, level + 1)

    for root in tree:
        flatten(root)

    return flat_list


def get_folders_tree_flat(request, page):
    """Get folders as flat list with hierarchy info for template rendering.

    This returns all folders as siblings (no DOM nesting) while preserving
    hierarchy information via level and parent_id attributes. Includes
    is_expanded and is_visible for server-side expand state.

    Args:
        request: The HTTP request object
        page: The page type (tasks, notes, contacts, favorites)

    Returns:
        list: Flat list of dicts with folder, level, parent_id, has_children,
              is_expanded, is_visible keys
    """
    tree = get_folders_tree(request, page)
    flat_list = []

    # Get user's expanded folders for this page
    user_expanded = request.user.expanded_folders
    if isinstance(user_expanded, dict):
        expanded_ids = set(user_expanded.get(page, []))
    else:
        expanded_ids = set()

    def flatten(node, level=0, parent_id=None, parent_expanded=True):
        folder = node["folder"]
        is_expanded = folder.id in expanded_ids
        # Root folders (level 0) are always visible; children visible if parent is expanded
        is_visible = (level == 0) or parent_expanded

        flat_list.append(
            {
                "folder": folder,
                "level": level,
                "parent_id": parent_id,
                "has_children": bool(node["children"]),
                "is_expanded": is_expanded,
                "is_visible": is_visible,
            }
        )
        for child in node["children"]:
            flatten(child, level + 1, folder.id, is_expanded)

    for root in tree:
        flatten(root)

    return flat_list


def get_task_folders(request):
    """Get task folders (wrapper for backward compatibility).

    Args:
        request: The HTTP request object

    Returns:
        QuerySet: Task folders the user can access
    """
    return get_folders_for_page(request, "tasks")


def select_folder(request, page):
    """Get the user's currently selected folder for a page.

    Args:
        request: The HTTP request object
        page: The page type (tasks, notes, contacts, favorites)

    Returns:
        Folder or None: The selected folder, or None if not set
    """
    user = request.user
    folder_id = getattr(user, page + "_folder")

    if folder_id and folder_id > 0:
        try:
            accessible_ids = get_accessible_folder_ids(user, page)
            folder = Folder.objects.filter(pk=folder_id, id__in=accessible_ids).first()

            if not folder:
                # Folder doesn't exist or user doesn't have access
                setattr(user, page + "_folder", 0)
                user.save()
                folder = None
        except Exception:
            setattr(user, page + "_folder", 0)
            user.save()
            folder = None
    else:
        folder = None

    return folder


def get_valid_parent_folders(request, page, exclude_folder=None):
    """Get folders that can be valid parents (depth 0 or 1, owned by user).

    Args:
        request: The HTTP request object
        page: The page type (tasks, notes, contacts, favorites)
        exclude_folder: Optional folder to exclude (and its descendants)

    Returns:
        QuerySet: Folders that can serve as parents
    """
    user = request.user
    folders = Folder.objects.filter(
        page=page,
        user=user,  # Only own folders can be parents
        depth__lt=2,  # Can only be parent if depth is 0 or 1
    )

    if exclude_folder and exclude_folder.pk:
        # Exclude the folder itself and its descendants
        exclude_ids = [exclude_folder.id] + [
            d.id for d in exclude_folder.get_descendants()
        ]
        folders = folders.exclude(id__in=exclude_ids)

    return folders.order_by("name")
