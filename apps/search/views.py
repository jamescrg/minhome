
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from apps.contacts.models import Contact
from apps.notes.models import Note
from apps.folders.models import Folder
from apps.favorites.models import Favorite


@login_required
def index(request):
    """Display the form to enter a search query. """

    context = {
        'page': 'search',
        'action': '/search/results',
        'results': False,
    }
    return render(request, 'search/content.html', context)


@login_required
def results(request):
    """Run the search query and display the results."""

    user = request.user
    text = request.POST.get('search_text')

    favorites = Favorite.objects.filter(user=user)
    favorites = favorites.filter(
        Q(name__icontains=text)
        | Q(url__icontains=text)
        | Q(description__icontains=text)
    ).order_by('name')
    for favorite in favorites:
        favorite.folder = Folder.objects.filter(pk=favorite.folder_id).first()

    contacts = Contact.objects.filter(user=user)
    contacts = contacts.filter(
        Q(name__contains=text)
        | Q(company__icontains=text)
        | Q(address__icontains=text)
        | Q(phone1__icontains=text)
        | Q(phone2__icontains=text)
        | Q(phone3__icontains=text)
        | Q(email__icontains=text)
        | Q(website__icontains=text)
        | Q(notes__icontains=text)
    ).order_by('name')
    for contact in contacts:
        contact.folder = Folder.objects.filter(pk=contact.folder_id).first()

    notes = Note.objects.filter(user=user)
    notes = notes.filter(Q(subject__icontains=text) | Q(note__icontains=text)).order_by(
        'subject'
    )
    for note in notes:
        note.folder = Folder.objects.filter(pk=note.folder_id).first()

    context = {
        'page': 'search',
        'action': '/search/results',
        'results': True,
        'favorites': favorites,
        'contacts': contacts,
        'notes': notes,
    }

    return render(request, 'search/content.html', context)
