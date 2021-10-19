
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
        'page': page,
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
def add(request):

    user_id = request.user.id
    folders = Folder.objects.filter(user_id=user_id, page='notes').order_by('name')
    selected_folder = folders.filter(selected=1).get()

    if request.method == 'POST':

        # create a bound note form loaded with the post values
        # this will render even if the post values are invalid
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user_id = user_id
            note.save()

            # deselect previously selected note
            old = Note.objects.filter(user_id=user_id, selected=1).get()
            if old:
                old.selected = 0
                old.save()

            # select newest note for user
            new = Note.objects.filter(user_id=user_id).latest('id')
            new.selected = 1
            new.save()

            return redirect('notes')

    else:

        # request is a get request
        # create unbound note form
        form = NoteForm(initial={'folder': selected_folder.id})

    # set the initial range of values for folder attribute
    form.fields['folder'].queryset = Folder.objects.filter(
            user_id=user_id, page='notes').order_by('name')

    context = {
        'page': 'notes',
        'edit': False,
        'add': True,
        'folders': folders,
        'action': '/notes/add',
        'form': form,
    }

    return render(request, 'notes/content.html', context)


@login_required
def edit(request, id):

    user_id = request.user.id
    folders = Folder.objects.filter(user_id=user_id, page='notes').order_by('name')
    selected_folder = folders.filter(selected=1).get()
    note = get_object_or_404(Note, pk=id)

    if request.method == 'POST':

        try:
            note = Note.objects.filter(user_id=request.user.id, pk=id).get()
        except:
            raise Http404('Record not found.')

        form = NoteForm(request.POST, instance=note)

        if form.is_valid():

            note = form.save(commit=False)
            note.user_id = user_id
            note.save()
            return redirect('notes')

    else:

        form = NoteForm(instance=note, initial={'folder': selected_folder.id})

    form.fields['folder'].queryset = Folder.objects.filter(
            user_id=user_id, page='notes').order_by('name')

    context = {
        'page': 'notes',
        'edit': True,
        'add': False,
        'folders': folders,
        'action': f'/notes/{id}/edit',
        'form': form,
        'note': note,
    }

    return render(request, 'notes/content.html', context)


@login_required
def delete(request, id):
    try:
        note = Note.objects.filter(user_id=request.user.id, pk=id).get()
    except:
        raise Http404('Record not found.')
    note.delete()
    return redirect('notes')
