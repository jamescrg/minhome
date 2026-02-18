from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.folders.folders import get_folders_for_page
from apps.management.pagination import CustomPaginator

from .forms import NoteForm
from .models import Note

SIDEBAR_SORT_OPTIONS = [
    ("-updated_at", "Modified, new to old"),
    ("-created_at", "Created, new to old"),
    ("title", "Title (A-Z)"),
]


def get_notes_data(request):
    """Get notes data with filters applied from session."""
    filter_data = request.session.get("notes_filter", {})

    queryset = Note.objects.filter(user=request.user)

    # Folder filter
    folder_id = filter_data.get("folder_id")
    selected_folder_id = None
    selected_folder_name = ""
    if folder_id:
        try:
            folder_id = int(folder_id)
            queryset = queryset.filter(folder_id=folder_id)
            selected_folder_id = folder_id
            from apps.folders.models import Folder

            folder = Folder.objects.filter(pk=folder_id).first()
            if folder:
                selected_folder_name = folder.name
        except (ValueError, TypeError):
            pass

    # Keyword filter
    keyword = filter_data.get("keyword", "")
    if keyword:
        queryset = queryset.filter(title__icontains=keyword)

    # Ordering
    current_order = filter_data.get("order_by", "-updated_at")
    queryset = queryset.order_by(current_order)

    # Folders for dropdown
    folders = get_folders_for_page(request, "notes")

    session_key = "notes_page"
    trigger_key = "notesChanged"
    pagination = CustomPaginator(queryset, 20, request, session_key)

    return {
        "notes": pagination.get_object_list(),
        "number_notes": queryset.count(),
        "current_order": current_order.lstrip("-"),
        "keyword": keyword,
        "selected_folder_id": selected_folder_id,
        "selected_folder_name": selected_folder_name,
        "folders": folders,
        "pagination": pagination,
        "session_key": session_key,
        "trigger_key": trigger_key,
    }


# =============================================================================
# List Views
# =============================================================================


@login_required
def notes_index(request):
    """Main notes list view."""
    context = {"page": "notes"} | get_notes_data(request)
    return render(request, "notes/main.html", context)


@login_required
def notes_list(request):
    """HTMX partial for notes list."""
    context = {"page": "notes"} | get_notes_data(request)
    return render(request, "notes/list.html", context)


@login_required
def notes_add(request):
    """Add a new note via modal."""
    if request.method == "POST":
        form = NoteForm(request.POST, request=request, use_required_attribute=False)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()

            note_url = reverse("notes:note-view", args=[note.id])
            return HttpResponse(
                f'<script>window.open("{note_url}", "_blank");'
                "window.dispatchEvent(new CustomEvent('close-modal'));</script>",
                headers={"HX-Trigger": "notesChanged"},
            )
    else:
        form = NoteForm(request=request, use_required_attribute=False)

    context = {
        "page": "notes",
        "form": form,
        "action": "Add",
        "folders": get_folders_for_page(request, "notes"),
    }
    return render(request, "notes/form.html", context)


@login_required
def notes_order_by(request, order):
    """Sort notes by field."""
    filter_data = request.session.get("notes_filter", {})

    current_order = filter_data.get("order_by", "")
    if current_order == order:
        new_order = f"-{order}" if not current_order.startswith("-") else order
    else:
        new_order = order

    filter_data["order_by"] = new_order
    request.session["notes_filter"] = filter_data
    request.session["notes_page"] = 1
    request.session.modified = True

    return redirect("notes:list")


@login_required
def notes_filter_folder(request, folder_id):
    """Filter notes by folder."""
    filter_data = request.session.get("notes_filter", {})
    filter_data["folder_id"] = folder_id
    request.session["notes_filter"] = filter_data
    request.session["notes_page"] = 1
    request.session.modified = True

    return redirect("notes:list")


@login_required
def notes_filter_folder_clear(request):
    """Clear folder filter."""
    filter_data = request.session.get("notes_filter", {})
    filter_data.pop("folder_id", None)
    request.session["notes_filter"] = filter_data
    request.session["notes_page"] = 1
    request.session.modified = True

    return redirect("notes:list")


@login_required
def notes_filter_keyword(request):
    """Filter notes by keyword."""
    filter_data = request.session.get("notes_filter", {})
    keyword = request.GET.get("keyword", "").strip()

    if keyword:
        filter_data["keyword"] = keyword
    else:
        filter_data.pop("keyword", None)

    request.session["notes_filter"] = filter_data
    request.session["notes_page"] = 1
    request.session.modified = True

    context = {"page": "notes"} | get_notes_data(request)
    return render(request, "notes/table.html", context)


# =============================================================================
# Editor Views
# =============================================================================


def get_sorted_notes(user, sort_order="-updated_at"):
    """Get notes sorted by specified order."""
    return Note.objects.filter(user=user).order_by(sort_order)[:20]


@login_required
def note_view(request, note_id):
    """Standalone editor view for a note."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    sort_order = request.session.get("notes_sidebar_sort", "-updated_at")
    notes = get_sorted_notes(request.user, sort_order)

    context = {
        "note": note,
        "notes": notes,
        "sidebar_sort_options": SIDEBAR_SORT_OPTIONS,
        "current_sort": sort_order,
    }
    return render(request, "notes/editor.html", context)


@login_required
def note_content_partial(request, note_id):
    """HTMX partial for switching notes in the editor."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(
        request,
        "notes/editor-content.html",
        {"note": note},
    )


@login_required
def sidebar_sort(request, note_id, sort_key):
    """Change sidebar sort order and return updated sidebar list."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    valid_keys = [key for key, _ in SIDEBAR_SORT_OPTIONS]
    if sort_key not in valid_keys:
        sort_key = "-updated_at"

    request.session["notes_sidebar_sort"] = sort_key

    notes = get_sorted_notes(request.user, sort_key)

    context = {
        "note": note,
        "notes": notes,
        "sidebar_sort_options": SIDEBAR_SORT_OPTIONS,
        "current_sort": sort_key,
    }
    return render(request, "notes/sidebar-list.html", context)


@login_required
def note_edit(request, note_id):
    """Edit note metadata (title + folder)."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    if request.method == "POST":
        form = NoteForm(
            request.POST, instance=note, request=request, use_required_attribute=False
        )
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "notesChanged"})
    else:
        form = NoteForm(instance=note, request=request, use_required_attribute=False)

    context = {
        "page": "notes",
        "note": note,
        "form": form,
        "action": "Edit",
        "folders": get_folders_for_page(request, "notes"),
    }
    return render(request, "notes/form.html", context)


@login_required
@require_POST
def note_delete(request, note_id):
    """Delete a note."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    note.delete()
    return HttpResponse(status=204, headers={"HX-Trigger": "notesChanged"})


@login_required
@require_POST
def note_autosave(request, note_id):
    """Autosave endpoint for the editor."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    content = request.POST.get("content", "")
    note.content = content
    update_fields = ["content", "updated_at"]

    is_encrypted = request.POST.get("is_encrypted")
    if is_encrypted is not None:
        note.is_encrypted = is_encrypted == "true"
        update_fields.append("is_encrypted")

    note.save(update_fields=update_fields)

    return JsonResponse({"saved": True, "updated_at": note.updated_at.isoformat()})


@login_required
@require_POST
def note_title(request, note_id):
    """Update note title."""
    note = get_object_or_404(Note, pk=note_id, user=request.user)

    title = request.POST.get("title", "").strip()
    if title:
        note.title = title
        note.save(update_fields=["title", "updated_at"])
        return JsonResponse({"saved": True, "title": note.title})

    return JsonResponse({"saved": False, "error": "Title cannot be empty"}, status=400)


@login_required
def notes_shortcuts(request):
    """Show keyboard shortcuts modal."""
    return render(request, "notes/shortcuts-modal.html")


@login_required
def note_import_modal(request, note_id):
    """Show import markdown modal."""
    return render(request, "notes/import-modal.html")
