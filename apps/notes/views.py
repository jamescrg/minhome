import json

import markdown
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.folders.folders import (
    get_folders_for_page,
    get_folders_tree_flat,
    get_valid_parent_folders,
    select_folder,
)
from apps.notes.forms import NoteForm
from apps.notes.models import Note


def _get_notes_context(request):
    """Helper to build context for notes partials."""
    user = request.user
    selected_folder = select_folder(request, "notes")

    if selected_folder:
        notes = Note.objects.filter(user=user, folder_id=selected_folder.id)
    else:
        notes = Note.objects.filter(user=user, folder_id__isnull=True)

    notes = notes.order_by("subject")

    selected_note_id = user.notes_note
    try:
        selected_note = Note.objects.filter(pk=selected_note_id).get()
        # Convert markdown to HTML for display
        selected_note.note = markdown.markdown(selected_note.note)
    except ObjectDoesNotExist:
        selected_note = None

    return {
        "page": "notes",
        "notes": notes,
        "selected_note": selected_note,
        "selected_folder": selected_folder,
    }


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

    folders = get_folders_for_page(request, page)

    selected_folder = select_folder(request, "notes")

    if selected_folder:
        notes = Note.objects.filter(user=user, folder_id=selected_folder.id)
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
        "folders": folders,
        "folder_tree_flat": get_folders_tree_flat(request, page),
        "valid_parent_folders": get_valid_parent_folders(request, page),
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

    if request.method == "POST":
        # create a bound note form loaded with the post values
        # this will render even if the post values are invalid
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
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

        if selected_folder:
            form = NoteForm(initial={"folder": selected_folder.id})
        else:
            form = NoteForm()

    # set the initial range of values for folder attribute
    form.fields["folder"].queryset = get_folders_for_page(request, "notes")

    context = {
        "page": "notes",
        "edit": False,
        "add": True,
        "folders": folders,
        "folder_tree_flat": get_folders_tree_flat(request, "notes"),
        "valid_parent_folders": get_valid_parent_folders(request, "notes"),
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
    folders = get_folders_for_page(request, "notes")

    selected_folder = select_folder(request, "notes")

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
        if selected_folder:
            form = NoteForm(instance=note, initial={"folder": selected_folder.id})
        else:
            form = NoteForm(instance=note)

    form.fields["folder"].queryset = get_folders_for_page(request, "notes")

    context = {
        "page": "notes",
        "edit": True,
        "add": False,
        "folders": folders,
        "folder_tree_flat": get_folders_tree_flat(request, "notes"),
        "valid_parent_folders": get_valid_parent_folders(request, "notes"),
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


# HTMX Views


@login_required
def notes_list_htmx(request):
    """Return notes list partial for htmx."""
    context = _get_notes_context(request)
    return render(request, "notes/list.html", context)


@login_required
def note_detail_htmx(request):
    """Return note detail partial for htmx."""
    context = _get_notes_context(request)
    if context["selected_note"]:
        return render(request, "notes/note.html", context)
    return HttpResponse("")


@login_required
def select_htmx(request, id):
    """Select note via htmx, return detail + updated list (oob)."""
    user = request.user
    user.notes_note = id
    user.save()

    context = _get_notes_context(request)
    return render(request, "notes/note-with-list-oob.html", context)


@login_required
def notes_form_htmx(request, id=None):
    """Return note form in modal for htmx, or process form submission."""
    user = request.user
    note = None

    if id:
        try:
            note = Note.objects.filter(user=user, pk=id).get()
        except ObjectDoesNotExist:
            raise Http404("Record not found.")

    if request.method == "POST":
        if note:
            form = NoteForm(request.POST, instance=note)
        else:
            form = NoteForm(request.POST)

        form.fields["folder"].queryset = get_folders_for_page(request, "notes")

        if form.is_valid():
            saved_note = form.save(commit=False)
            saved_note.user = user
            saved_note.save()

            # Select the saved note
            user.notes_note = saved_note.id
            user.save()

            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"notesChanged": "", "noteDetailChanged": ""}
                    )
                },
            )
    else:
        if note:
            form = NoteForm(instance=note)
        else:
            form = NoteForm()

    context = {
        "page": "notes",
        "edit": id is not None,
        "note": note,
        "form": form,
        "action": f"/notes/{id}/form-htmx" if id else "/notes/form-htmx",
        "folder_tree_flat": get_folders_tree_flat(request, "notes"),
    }

    return render(request, "notes/modal-form.html", context)


@login_required
def delete_htmx(request, id):
    """Delete note via htmx."""
    user = request.user

    try:
        note = Note.objects.filter(user=user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")

    note.delete()

    # Clear selected note
    user.notes_note = 0
    user.save()

    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps({"notesChanged": "", "noteDetailChanged": ""})
        },
    )
