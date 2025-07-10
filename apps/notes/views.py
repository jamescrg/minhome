import markdown
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from apps.folders.folders import select_folder, get_folders_for_page, get_breadcrumbs, get_folder_tree
from apps.folders.models import Folder
from apps.notes.forms import NoteForm
from apps.notes.models import Note


@login_required
def index(request):
    """Display a list of folders and notes, along with a note.

    Notes:
        Always displays folders.
        If a folder is selected, displays the notes for a folder.
        If a note is selected, displays the note.

    """

    user = request.user
    page = "notes"

    selected_folder = select_folder(request, "notes")

    # Get folder tree starting from selected folder
    folder_tree, tree_has_children = get_folder_tree(request, page, selected_folder)

    if selected_folder:
        # Get notes from selected folder only
        notes = Note.objects.filter(user=user, folder=selected_folder)
    else:
        notes = Note.objects.filter(user=user, folder_id__isnull=True)

    notes = notes.order_by("subject")

    selected_note_id = request.user.notes_note

    try:
        selected_note = Note.objects.filter(pk=selected_note_id).get()
    except ObjectDoesNotExist:
        selected_note = None

    if selected_note:
        selected_note.note = markdown.markdown(selected_note.note)

    context = {
        "page": page,
        "edit": False,
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
        "selected_folder": selected_folder,
        "notes": notes,
        "selected_note": selected_note,
    }

    return render(request, "notes/content.html", context)


@login_required
def select(request, id):
    """Select a note for display, redirect to index.

    Args:
        id (int): a Note instance id

    """
    user = request.user
    user.notes_note = id
    user.save()
    return redirect("/notes/")


@login_required
def add(request):
    """Add a new note.

    Notes:
        GET: Display new note form.
        POST: Add note to database.

    """

    user = request.user
    folders = get_folders_for_page(request, "notes")

    selected_folder = select_folder(request, "notes")

    folder_tree, tree_has_children = get_folder_tree(
        request, "notes", selected_folder)

    if request.method == "POST":
        # create a bound note form loaded with the post values
        # this will render even if the post values are invalid
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.folder = selected_folder  # Always assign to selected folder
            note.save()

            # deselect previously selected note
            try:
                old = Note.objects.filter(user=user, selected=1).get()
            except Note.DoesNotExist:
                pass
            else:
                old.selected = 0
                old.save()

            # select newest note for user
            new = Note.objects.filter(user=user).latest("id")
            new.selected = 1
            new.save()

            return redirect("notes")

    else:
        # request is a get request
        # create unbound note form
        form = NoteForm()

    context = {
        "page": "notes",
        "edit": False,
        "add": True,
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
        "selected_folder": selected_folder,
        "action": "/notes/add",
        "form": form,
    }

    return render(request, "notes/content.html", context)


@login_required
def edit(request, id):
    """Edit a note.

    Args:
        id (int): A Note instance id

    Notes:
        GET: Display note form.
        POST: Update note in database.
    """

    user = request.user
    selected_folder = select_folder(request, "notes")

    folder_tree, tree_has_children = get_folder_tree(
        request, "notes", selected_folder)

    note = get_object_or_404(Note, pk=id)

    if request.method == "POST":
        try:
            note = Note.objects.filter(user=request.user, pk=id).get()
        except ObjectDoesNotExist:
            raise Http404("Record not found.")

        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.save()
            return redirect("notes")

    else:
        form = NoteForm(instance=note)

        context = {
            "page": "notes",
            "edit": True,
            "add": False,
            "folder_tree": folder_tree,
            "tree_has_children": tree_has_children,
            "selected_folder": selected_folder,
            "action": f"/notes/{id}/edit",
            "form": form,
            "note": note,
        }

    return render(request, "notes/content.html", context)


@login_required
def delete(request, id):
    """Delete a note.

    Args:
        id (int):  a Note instance id

    """
    try:
        note = Note.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")
    note.delete()
    return redirect("notes")


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def move_to_folder(request):
    """Move a note to a different folder.

    Expected POST data:
        item_id: ID of the note to move
        folder_id: ID of the target folder
    """
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        folder_id = data.get('folder_id')

        if not item_id or not folder_id:
            return JsonResponse({'success': False, 'message': 'Missing required parameters'})

        # Get the note
        note = get_object_or_404(Note, pk=item_id, user=request.user)

        # Get the target folder
        folder = get_object_or_404(Folder, pk=folder_id, user=request.user)

        # Move the note to the new folder
        note.folder = folder
        note.save()

        return JsonResponse({'success': True, 'message': 'Note moved successfully'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
