
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from apps.notes.models import Note
from apps.notes.forms import NoteForm
from apps.folders.models import Folder


@login_required
def index(request):

    user_id = request.user.id
    page = 'notes'

    folders = Folder.objects.filter(user_id=user_id, page=page).order_by('name')

    selected_folder = Folder.objects.filter(
        user_id=user_id, page=page, selected=1
    ).first()

    if selected_folder:
        notes = Note.objects.filter(user_id=user_id, folder_id=selected_folder.id)
    else:
        notes = Note.objects.filter(user_id=user_id, folder_id__isnull=True)

    notes = notes.order_by('subject')

    selected_note = Note.objects.filter(user_id=user_id, selected=1).first()

    context = {
        'page': 'notes',
        'edit': False,
        'folders': folders,
        'selected_folder': selected_folder,
        'notes': notes,
        'selected_note': selected_note,
    }

    return render(request, 'notes/content.html', context)


@login_required
def select(request, id):
    user_id = request.user.id
    old = Note.objects.filter(user_id=user_id, selected=1).update(selected=0)
    new = get_object_or_404(Note, pk=id)
    new.selected = 1
    new.save()
    return redirect('/notes/')


@login_required
def new(request, folder_id):

    user_id = request.user.id

    if request.method == 'POST':

        # create new note
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = user_id
            note.save()

        # deselect previously selected note
        try:
            old = Note.objects.filter(user_id=user_id, selected=1).get()
            old.selected = 0
            old.save()
        except:
            pass

        # select newest note for user
        new = Note.objects.filter(user_id=user_id).latest('id')
        new.selected = 1
        new.save()

        return redirect('notes')

    else:

        user_id = request.user.id
        selected_folder_id = folder_id
        selected_folder = get_object_or_404(Folder, pk=folder_id)
        folders = Folder.objects.filter(user_id=user_id, page='notes').order_by('name')

        form = NoteForm(initial={'folder': selected_folder_id})
        form.fields['folder'].queryset = Folder.objects.filter(
                user_id=user_id, page='notes').order_by('name')

        context = {
            'page': 'notes',
            'edit': False,
            'add': True,
            'action': f'/notes/{selected_folder_id}/new',
            'folders': folders,
            'selected_folder': selected_folder,
            'selected_folder_id': selected_folder_id,
            'form': form,
        }

        return render(request, 'notes/content.html', context)


@login_required
def edit(request, id):
    user_id = request.user.id
    note = get_object_or_404(Note, pk=id)
    folders = Folder.objects.filter(user_id=user_id, page='notes').order_by('name')
    selected_folder_id = note.folder_id
    selected_folder = get_object_or_404(Folder, pk=selected_folder_id)

    context = {
        'page': 'notes',
        'edit': True,
        'add': False,
        'action': f'/notes/update/{id}',
        'folders': folders,
        'selected_folder': selected_folder,
        'selected_folder_id': selected_folder_id,
        'note': note,
        'phone_labels': ['Mobile', 'Home', 'Work', 'Fax', 'Other'],
    }
    return render(request, 'notes/content.html', context)


@login_required
def update(request, id):
    try:
        note = Note.objects.filter(user_id=request.user.id, pk=id).get()
    except:
        raise Http404('Record not found.')
    for field in note.fillable:
        setattr(note, field, request.POST.get(field))
    note.save()
    return redirect('notes')


@login_required
def delete(request, id):
    try:
        note = Note.objects.filter(user_id=request.user.id, pk=id).get()
    except:
        raise Http404('Record not found.')
    note.delete()
    return redirect('notes')
