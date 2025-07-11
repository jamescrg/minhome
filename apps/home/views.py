from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import apps.home.google as google
from apps.favorites.models import Favorite
from apps.folders.models import Folder
from apps.home.movement import sequence
from apps.home.toggle import show_section
from apps.tasks.models import Task


def get_search_context(user):
    """Get search engine context for a user"""
    engines = [
        {"id": "google", "name": "Google", "url": "google.com/search"},
        {"id": "duckduckgo", "name": "DuckDuckGo", "url": "duckduckgo.com/"},
        {"id": "wikipedia", "name": "Wikipedia", "url": "en.wikipedia.org/w/index.php"},
        {"id": "bing", "name": "Bing", "url": "bing.com/"},
    ]

    search_engine = "google"
    for engine in engines:
        if engine["id"] == user.search_engine:
            search_engine = engine

    return {
        "engines": engines,
        "search_engine": search_engine,
    }


@login_required
def index(request):
    """Display the home page.

    Notes:
        Displays upcoming events, current tasks, and priority favorites

    """

    user = request.user

    # EVENTS
    # ----------------

    # check whether events are shown are hidden
    show_events = show_section(user, "events")

    # if events are shown, load them
    if show_events:

        # only show events if the user has connected a Google account
        if user.google_credentials:

            # load the events from Google
            events = google.get_events(user.id)

        else:
            events = None
    else:
        events = None

    # TASKS
    # ----------------

    # check whether tasks are shown or hidden
    show_tasks = show_section(user, "tasks")

    # if tasks are shown, check for task_folders
    # Get all task folders that user has access to (owned or shared)
    # Include all folders to show child folders with home_column values
    all_task_folders = Folder.objects.filter(page="tasks").filter(
        Q(user=user) | Q(editors=user)
    )
    task_folders = all_task_folders.filter(home_column__gt=1)
    if task_folders:

        # eliminate folders with no tasks
        for folder in task_folders:
            tasks = Task.objects.filter(folder_id=folder.id).exclude(status=1)
            if not tasks:
                task_folders = task_folders.exclude(id=folder.id)

        # attatch tasks to folders with tasks
        for folder in task_folders:
            tasks = Task.objects.filter(folder_id=folder.id).exclude(status=1)
            tasks = tasks.order_by("status", "title")
            folder.tasks = tasks

    # check whether there are some tasks in any of the folders
    # if so, flag as true
    # the purpose of this flag is to show the tasks area
    # only if there are at least some unchecked tasks to display
    some_tasks = False
    if task_folders:
        for folder in task_folders:
            if folder.tasks:
                some_tasks = True

    # SEARCH
    # ----------------
    search_context = get_search_context(user)

    # FAVORITES
    # ----------------

    columns = []
    for i in range(1, 6):
        # Get all favorites folders that user has access to (owned or shared)
        # Include all folders to show child folders with home_column values
        all_favorites_folders = Folder.objects.filter(page="favorites").filter(
            Q(user=user) | Q(editors=user)
        )
        folders = all_favorites_folders.filter(home_column=i)
        folders = folders.order_by("home_rank")
        for folder in folders:
            favorites = Favorite.objects.filter(folder_id=folder.id, home_rank__gt=0)
            favorites = favorites.order_by("home_rank")
            folder.favorites = favorites
        columns.append(folders)

    moved_folder = request.session.get("moved_folder", 0)
    if moved_folder:
        request.session["moved_folder"] = 0

    context = {
        "page": "home",
        "origin": "home",
        "show_tasks": show_tasks,
        "task_folders": task_folders,
        "some_tasks": some_tasks,
        "events": events,
        "show_events": show_events,
        "columns": columns,
        "moved_folder": moved_folder,
    }

    # Add search context
    context.update(search_context)

    return render(request, "home/content.html", context)


@login_required
def toggle(request, section):
    """Toggle on or off various sections of the home page.

    Args:
        section (str): the section to toggle

    Notes:
        Page sections appear in the morning, this turns them off

        Session based, so that sections are only turned off for
        the specific browser from whcih they are toggled

    """

    user = request.user

    attrib = f"home_{section}_hidden"
    if getattr(user, attrib):
        setattr(user, attrib, None)
    else:
        setattr(user, attrib, date.today())

    user.save()

    return redirect("home")


@login_required
def folder(request, id, direction):
    """Move a folder up, down, left, or right

    Args:
        id (int): the folder to be moved
        direction (str): the direction in which to move the folder

    Notes:
        The home page has four columns. This function moves folders
        from one column to another, or up and down in an specific column.

    """

    user = request.user

    # if the stack order is being changed
    if direction == "up" or direction == "down":
        # get the folder to be moved
        # identify the column to which it belongs
        moved_folder = get_object_or_404(Folder, pk=id)
        origin_column = moved_folder.home_column

        # make sure the folders are sequential and adjacent
        sequence(user, origin_column)

        # identify the origin rank as modified by the sequence operation
        origin_rank = moved_folder.home_rank

        # identify the destination rank
        if direction == "up":
            destination_rank = origin_rank - 1
        if direction == "down":
            destination_rank = origin_rank + 1

        # identify the folder to be displaced
        try:
            displaced_folder = Folder.objects.filter(
                user=user,
                page="favorites",
                home_column=origin_column,
                home_rank=destination_rank,
            ).get()
        except Folder.DoesNotExist:
            displaced_folder = False

        # if a folder is being displaced, move it and the original folder
        if displaced_folder:
            moved_folder.home_rank = destination_rank
            moved_folder.save()
            displaced_folder.home_rank = origin_rank
            displaced_folder.save()

    # if the column is being changed
    if direction == "left" or direction == "right":
        # get the folder to be moved, along with its column and rank
        moved_folder = get_object_or_404(Folder, pk=id)
        origin_column = moved_folder.home_column

        if direction == "left" and origin_column > 1:
            destination_column = origin_column - 1
        elif direction == "right" and origin_column < 5:
            destination_column = origin_column + 1
        else:
            destination_column = origin_column

        if destination_column != origin_column:

            # sequence destination column
            # make sure the folders are sequential and adjacent
            folders = sequence(user, destination_column)

            # increment all up by one if greater than or equal to moved_folder
            for folder in folders:
                if folder.home_rank >= moved_folder.home_rank:
                    folder.home_rank = folder.home_rank + 1
                    folder.save()

            # move over origin folder to destination column in first position
            moved_folder.home_column = destination_column
            moved_folder.home_rank = 1
            moved_folder.save()

        # resequence origin column
        # make sure the folders are sequential and adjacent
        sequence(user, origin_column)

    # save the id of the moved folder for the next page view
    request.session["moved_folder"] = moved_folder.id

    return redirect("home")


@login_required
def favorite(request, id, direction):
    """Move a favorite up or down.

    Args:
        id (int): the favorite to be moved
        direction (str): the direction in which to move the favorite

    """

    user = request.user

    # get the favorite to be moved
    moved_favorite = get_object_or_404(Favorite, pk=id)
    folder_id = moved_favorite.folder_id

    # make sure the favorites are sequential and adjacent
    favorites = Favorite.objects.filter(user=user, folder_id=folder_id, home_rank__gt=0)
    favorites = favorites.order_by("home_rank")

    count = 1
    for favorite in favorites:
        favorite.home_rank = count
        favorite.save()
        count += 1

    favorites = Favorite.objects.filter(user=user, folder_id=folder_id, home_rank__gt=0)
    favorites = favorites.order_by("home_rank")

    # identify the origin rank as modified by the sequence operation
    moved_favorite = get_object_or_404(Favorite, pk=id)
    origin_rank = moved_favorite.home_rank

    # identify the destination rank
    if direction == "up":
        destination_rank = origin_rank - 1
    if direction == "down":
        destination_rank = origin_rank + 1

    # identify the favorite to be displaced
    displaced_favorite = Favorite.objects.filter(
        user=user, folder_id=folder_id, home_rank=destination_rank
    ).first()

    # if a favorite is being displaced, move it and the original favorite
    # otherwise, we are at the end of the column, make no changes

    # make sure the top favorite doesn't move if the user attempts to move it up
    if destination_rank > 0:
        moved_favorite.home_rank = destination_rank
        moved_favorite.save()

    if displaced_favorite:
        displaced_favorite.home_rank = origin_rank
        displaced_favorite.save()

    # save the id of the moved folder for the next page view
    request.session["moved_folder"] = moved_favorite.folder.id

    return redirect("home")


@login_required
def update_folder_column(request):
    """Update folder column and/or position via AJAX for drag-and-drop functionality.

    Expected POST data:
        folder_id: ID of the folder to move
        target_column: Column number (1-5) to move the folder to
        target_position: Optional position within the column (0-based index)
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    try:
        folder_id = int(request.POST.get("folder_id"))
        target_column = int(request.POST.get("target_column"))
        target_position = request.POST.get("target_position")

        # Validate target column
        if not (1 <= target_column <= 5):
            return JsonResponse({"success": False, "error": "Invalid target column"})

        # Get the folder to be moved
        moved_folder = get_object_or_404(
            Folder, pk=folder_id, user=request.user, page="favorites"
        )
        origin_column = moved_folder.home_column

        # Handle intra-column reordering (same column, different position)
        if target_column == origin_column and target_position is not None:
            try:
                target_position = int(target_position)

                # Get all folders in the same column
                column_folders = Folder.objects.filter(
                    user=request.user, page="favorites", home_column=target_column
                ).order_by("home_rank")

                folders_list = list(column_folders)

                # Remove the moved folder from its current position
                moved_folder_index = None
                for i, folder in enumerate(folders_list):
                    if folder.id == folder_id:
                        moved_folder_index = i
                        break

                if moved_folder_index is not None:
                    folders_list.pop(moved_folder_index)

                    # Insert at new position
                    target_position = min(target_position, len(folders_list))
                    folders_list.insert(target_position, moved_folder)

                    # Update ranks for all folders in the column
                    for i, folder in enumerate(folders_list):
                        folder.home_rank = i + 1
                        folder.save()

                    return JsonResponse(
                        {
                            "success": True,
                            "message": f"Folder reordered within column {target_column}",
                            "new_column": target_column,
                            "new_rank": target_position + 1,
                        }
                    )

            except (ValueError, TypeError):
                return JsonResponse(
                    {"success": False, "error": "Invalid target position"}
                )

        # Handle inter-column movement (different column)
        elif target_column != origin_column:
            # Sequence destination column - make sure folders are sequential
            sequence(request.user, target_column)

            # Determine target rank within destination column
            if target_position is not None:
                try:
                    target_position = int(target_position)
                    destination_folders = list(
                        Folder.objects.filter(
                            user=request.user,
                            page="favorites",
                            home_column=target_column,
                        ).order_by("home_rank")
                    )

                    # Insert at specified position
                    target_position = min(target_position, len(destination_folders))
                    new_rank = target_position + 1

                    # Shift existing folders down to make room
                    for folder in destination_folders[target_position:]:
                        folder.home_rank += 1
                        folder.save()

                except (ValueError, TypeError):
                    # Default to end of column if position is invalid
                    destination_folders = Folder.objects.filter(
                        user=request.user, page="favorites", home_column=target_column
                    ).order_by("home_rank")

                    if destination_folders:
                        new_rank = destination_folders.last().home_rank + 1
                    else:
                        new_rank = 1
            else:
                # Default to end of column
                destination_folders = Folder.objects.filter(
                    user=request.user, page="favorites", home_column=target_column
                ).order_by("home_rank")

                if destination_folders:
                    new_rank = destination_folders.last().home_rank + 1
                else:
                    new_rank = 1

            # Update the moved folder
            moved_folder.home_column = target_column
            moved_folder.home_rank = new_rank
            moved_folder.save()

            # Resequence origin column
            sequence(request.user, origin_column)

            return JsonResponse(
                {
                    "success": True,
                    "message": f"Folder moved to column {target_column}",
                    "new_column": target_column,
                    "new_rank": new_rank,
                }
            )
        else:
            return JsonResponse({"success": True, "message": "No change needed"})

    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid parameters"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def swap_folder_positions(request):
    """Swap the positions of two folders within the same column via AJAX.

    Expected POST data:
        dragged_folder_id: ID of the folder being dragged
        target_folder_id: ID of the folder being dropped onto
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    try:
        dragged_folder_id = int(request.POST.get("dragged_folder_id"))
        target_folder_id = int(request.POST.get("target_folder_id"))

        # Get both folders and ensure they belong to the user
        dragged_folder = get_object_or_404(
            Folder, pk=dragged_folder_id, user=request.user, page="favorites"
        )
        target_folder = get_object_or_404(
            Folder, pk=target_folder_id, user=request.user, page="favorites"
        )

        # Ensure folders are in the same column
        if dragged_folder.home_column != target_folder.home_column:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Folders must be in the same column to swap",
                }
            )

        # Swap the home_rank values
        dragged_rank = dragged_folder.home_rank
        target_rank = target_folder.home_rank

        dragged_folder.home_rank = target_rank
        target_folder.home_rank = dragged_rank

        dragged_folder.save()
        target_folder.save()

        return JsonResponse(
            {
                "success": True,
                "message": f"Swapped folder positions in column {dragged_folder.home_column}",
                "dragged_folder": {
                    "id": dragged_folder.id,
                    "new_rank": dragged_folder.home_rank,
                },
                "target_folder": {
                    "id": target_folder.id,
                    "new_rank": target_folder.home_rank,
                },
            }
        )

    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid folder IDs"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def insert_folder_at_position(request):
    """Insert a folder at the position of another folder, shifting others down.

    Expected POST data:
        dragged_folder_id: ID of the folder being moved
        target_folder_id: ID of the folder whose position we want to take
        target_column: Column number where the target folder is located
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    try:
        dragged_folder_id = int(request.POST.get("dragged_folder_id"))
        target_folder_id = int(request.POST.get("target_folder_id"))
        target_column = int(request.POST.get("target_column"))

        # Get both folders and ensure they belong to the user
        dragged_folder = get_object_or_404(
            Folder, pk=dragged_folder_id, user=request.user, page="favorites"
        )
        target_folder = get_object_or_404(
            Folder, pk=target_folder_id, user=request.user, page="favorites"
        )

        # Validate target column
        if not (1 <= target_column <= 5):
            return JsonResponse({"success": False, "error": "Invalid target column"})

        # Store original position info
        origin_column = dragged_folder.home_column
        target_rank = target_folder.home_rank

        # Adjust the target rank
        target_rank = target_folder.home_rank

        # Step 1: Get all folders in the target column at or after the target position
        folders_to_shift = Folder.objects.filter(
            user=request.user,
            page="favorites",
            home_column=target_column,
            home_rank__gte=target_rank,
        ).order_by("home_rank")

        # Step 2: Shift all folders down by 1 to make room
        for folder in folders_to_shift:
            folder.home_rank += 1
            folder.save()

        # Step 3: Move the dragged folder to the target position
        dragged_folder.home_column = target_column
        dragged_folder.home_rank = target_rank
        dragged_folder.save()

        # Step 4: Resequence the origin column to close the gap
        if origin_column != target_column:
            sequence(request.user, origin_column)

        return JsonResponse(
            {
                "success": True,
                "message": f"Inserted folder at position {target_rank} in column {target_column}",
                "moved_folder": {
                    "id": dragged_folder.id,
                    "new_column": target_column,
                    "new_rank": target_rank,
                },
            }
        )

    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid parameters"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def swap_favorite_positions(request):
    """Swap the positions of two favorites within the same folder via AJAX.

    Expected POST data:
        dragged_favorite_id: ID of the favorite being dragged
        target_favorite_id: ID of the favorite being dropped onto
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    try:
        dragged_favorite_id = int(request.POST.get("dragged_favorite_id"))
        target_favorite_id = int(request.POST.get("target_favorite_id"))

        # Import the Favorite model
        from apps.favorites.models import Favorite

        # Get both favorites and ensure they belong to the user
        dragged_favorite = get_object_or_404(
            Favorite, pk=dragged_favorite_id, user=request.user
        )
        target_favorite = get_object_or_404(
            Favorite, pk=target_favorite_id, user=request.user
        )

        # Ensure favorites are in the same folder
        if dragged_favorite.folder_id != target_favorite.folder_id:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Favorites must be in the same folder to swap",
                }
            )

        # Swap the home_rank values
        if hasattr(dragged_favorite, "home_rank") and hasattr(
            target_favorite, "home_rank"
        ):
            dragged_rank = dragged_favorite.home_rank
            target_rank = target_favorite.home_rank

            dragged_favorite.home_rank = target_rank
            target_favorite.home_rank = dragged_rank

            dragged_favorite.save()
            target_favorite.save()
        else:
            # If no home_rank field, we'll need a different approach
            # For now, return success but note that ordering might not persist
            pass

        return JsonResponse(
            {
                "success": True,
                "message": f"Swapped favorite positions in folder {dragged_favorite.folder_id}",
                "dragged_favorite": {
                    "id": dragged_favorite.id,
                    "name": dragged_favorite.name,
                },
                "target_favorite": {
                    "id": target_favorite.id,
                    "name": target_favorite.name,
                },
            }
        )

    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid favorite IDs"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def insert_favorite_at_position(request):
    """Insert a favorite at the position of another favorite, shifting others down.

    Expected POST data:
        dragged_favorite_id: ID of the favorite being moved
        target_favorite_id: ID of the favorite whose position we want to take
        insert_below: Whether to insert below the target favorite (true/false)
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    try:
        dragged_favorite_id = int(request.POST.get("dragged_favorite_id"))
        target_favorite_id = int(request.POST.get("target_favorite_id"))
        insert_below = request.POST.get("insert_below") == "true"

        # Import the Favorite model
        from apps.favorites.models import Favorite

        # Get both favorites and ensure they belong to the user
        dragged_favorite = get_object_or_404(
            Favorite, pk=dragged_favorite_id, user=request.user
        )
        target_favorite = get_object_or_404(
            Favorite, pk=target_favorite_id, user=request.user
        )

        # Ensure favorites are in the same folder
        if dragged_favorite.folder_id != target_favorite.folder_id:
            return JsonResponse(
                {"success": False, "error": "Favorites must be in the same folder"}
            )

        # Handle positioning using home_rank field
        if hasattr(dragged_favorite, "home_rank") and hasattr(
            target_favorite, "home_rank"
        ):
            target_rank = target_favorite.home_rank

            # If inserting below, adjust the target rank
            if insert_below:
                target_rank = target_favorite.home_rank + 1

            # Shift other favorites to make room
            favorites_to_shift = (
                Favorite.objects.filter(
                    user=request.user,
                    folder_id=target_favorite.folder_id,
                    home_rank__gte=target_rank,
                )
                .exclude(id=dragged_favorite_id)
                .order_by("home_rank")
            )

            for fav in favorites_to_shift:
                fav.home_rank += 1
                fav.save()

            # Move the dragged favorite to the target position
            dragged_favorite.home_rank = target_rank
            dragged_favorite.save()
        else:
            # If no home_rank field, we'll need a different approach
            # For now, return success but note that ordering might not persist
            pass

        return JsonResponse(
            {
                "success": True,
                "message": f"Inserted favorite at position in folder {dragged_favorite.folder_id}",
                "moved_favorite": {
                    "id": dragged_favorite.id,
                    "name": dragged_favorite.name,
                },
            }
        )

    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid parameters"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
def move_favorite_to_folder(request):
    """Move a favorite to a new folder and position it below a target favorite.

    Expected POST data:
        dragged_favorite_id: ID of the favorite being moved
        target_favorite_id: ID of the favorite to position below
        target_folder_id: ID of the folder to move to
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Only POST method allowed"})

    try:
        dragged_favorite_id = int(request.POST.get("dragged_favorite_id"))
        target_favorite_id = int(request.POST.get("target_favorite_id"))
        target_folder_id = int(request.POST.get("target_folder_id"))
        insert_below = request.POST.get("insert_below") == "true"

        # Import the Favorite model
        from apps.favorites.models import Favorite
        from apps.folders.models import Folder

        # Get the favorites and folder, ensure they belong to the user
        dragged_favorite = get_object_or_404(
            Favorite, pk=dragged_favorite_id, user=request.user
        )
        target_folder = get_object_or_404(
            Folder, pk=target_folder_id, user=request.user
        )

        # Handle empty folder case (target_favorite_id = -1)
        if target_favorite_id == -1:
            # Move to empty folder - just update folder and set home_rank to 1
            original_folder_id = dragged_favorite.folder_id
            dragged_favorite.folder_id = target_folder_id
            if hasattr(dragged_favorite, "home_rank"):
                dragged_favorite.home_rank = 1
            dragged_favorite.save()

            # Resequence the original folder if it's different
            if original_folder_id != target_folder_id:
                original_favorites = Favorite.objects.filter(
                    user=request.user, folder_id=original_folder_id, home_rank__gt=0
                ).order_by("home_rank")

                for index, fav in enumerate(original_favorites):
                    fav.home_rank = index + 1
                    fav.save()

            return JsonResponse(
                {
                    "success": True,
                    "message": f"Moved favorite to empty folder {target_folder_id}",
                    "moved_favorite": {
                        "id": dragged_favorite.id,
                        "name": dragged_favorite.name,
                        "new_folder_id": target_folder_id,
                        "new_rank": getattr(dragged_favorite, "home_rank", None),
                    },
                }
            )

        # Normal case with target favorite
        target_favorite = get_object_or_404(
            Favorite, pk=target_favorite_id, user=request.user
        )

        # Ensure target favorite is in the target folder
        if target_favorite.folder_id != target_folder_id:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Target favorite is not in the specified folder",
                }
            )

        # Store original folder for cleanup
        original_folder_id = dragged_favorite.folder_id

        # Handle positioning using home_rank field
        if hasattr(dragged_favorite, "home_rank") and hasattr(
            target_favorite, "home_rank"
        ):
            target_rank = target_favorite.home_rank

            # If inserting below, adjust the target rank
            if insert_below:
                target_rank = target_favorite.home_rank + 1

            # Shift other favorites in target folder to make room
            favorites_to_shift = Favorite.objects.filter(
                user=request.user,
                folder_id=target_folder_id,
                home_rank__gte=target_rank,
            ).order_by("home_rank")

            for fav in favorites_to_shift:
                fav.home_rank += 1
                fav.save()

            # Move the dragged favorite to the new folder and position
            dragged_favorite.folder_id = target_folder_id
            dragged_favorite.home_rank = target_rank
            dragged_favorite.save()

            # Resequence the original folder to close the gap
            if original_folder_id != target_folder_id:
                # Get only favorites that are visible on home page (home_rank > 0) and resequence
                original_favorites = Favorite.objects.filter(
                    user=request.user, folder_id=original_folder_id, home_rank__gt=0
                ).order_by("home_rank")

                for index, fav in enumerate(original_favorites):
                    fav.home_rank = index + 1
                    fav.save()
        else:
            # If no home_rank field, just move without positioning
            dragged_favorite.folder_id = target_folder_id
            dragged_favorite.save()

        return JsonResponse(
            {
                "success": True,
                "message": f'Moved favorite to folder {target_folder_id} at position {target_rank if "target_rank" in locals() else "end"}',
                "moved_favorite": {
                    "id": dragged_favorite.id,
                    "name": dragged_favorite.name,
                    "new_folder_id": target_folder_id,
                    "new_rank": getattr(dragged_favorite, "home_rank", None),
                },
            }
        )

    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid parameters"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
