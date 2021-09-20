from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from app.models import Folder, Contact
import app.google as google


@login_required
def index(request):
    user_id = request.user.id
    page = 'contacts'
    folders = Folder.objects.filter(user_id=user_id, page=page).order_by('name')
    selected_folder = Folder.objects.filter(
        user_id=user_id, page=page, selected=1
    ).first()

    if selected_folder:
        contacts = Contact.objects.filter(user_id=user_id, folder_id=selected_folder.id)
    else:
        contacts = Contact.objects.filter(user_id=user_id, folder_id=0)

    contacts = contacts.order_by('name')
    selected_contact = Contact.objects.filter(user_id=user_id, selected=1).first()
    if request.user.google_credentials:
        google = True
    else:
        google = False

    context = {
        'page': 'contacts',
        'edit': False,
        'folders': folders,
        'selected_folder': selected_folder,
        'contacts': contacts,
        'selected_contact': selected_contact,
        'google': google,
    }
    return render(request, 'contacts/content.html', context)


@login_required
def select(request, id):
    user_id = request.user.id
    old = Contact.objects.filter(user_id=user_id, selected=1).update(selected=0)
    new = get_object_or_404(Contact, pk=id)
    new.selected = 1
    new.save()
    return redirect('/contacts/')


@login_required
def add(request, id):
    user_id = request.user.id
    selected_folder_id = id
    selected_folder = get_object_or_404(Folder, pk=id)
    folders = Folder.objects.filter(user_id=user_id, page='contacts').order_by('name')
    contact = Contact()
    contact.folder_id = id

    context = {
        'page': 'contacts',
        'edit': False,
        'add': True,
        'action': '/contacts/insert',
        'folders': folders,
        'selected_folder': selected_folder,
        'selected_folder_id': selected_folder_id,
        'contact': contact,
        'phone_labels': ['Mobile', 'Home', 'Work', 'Fax', 'Other'],
    }

    return render(request, 'contacts/content.html', context)


@login_required
def insert(request):
    user = get_object_or_404(CustomUser, pk=request.user.id)

    contact = Contact()
    contact.user_id = user.id
    for field in contact.fillable:
        setattr(contact, field, request.POST.get(field))

    if user.google_credentials:
        contact.google_id = google.add_contact(contact)

    contact.save()

    return redirect('contacts')


@login_required
def edit(request, id):
    user_id = request.user.id
    contact = get_object_or_404(Contact, pk=id)
    folders = Folder.objects.filter(user_id=user_id, page='contacts').order_by('name')
    selected_folder_id = contact.folder_id
    selected_folder = get_object_or_404(Folder, pk=selected_folder_id)
    context = {
        'page': 'contacts',
        'edit': True,
        'add': False,
        'action': f'/contacts/update/{id}',
        'folders': folders,
        'selected_folder': selected_folder,
        'selected_folder_id': selected_folder_id,
        'contact': contact,
        'phone_labels': ['Mobile', 'Home', 'Work', 'Fax', 'Other'],
    }
    return render(request, 'contacts/content.html', context)


@login_required
def update(request, id):
    user = get_object_or_404(CustomUser, pk=request.user.id)

    try:
        contact = Contact.objects.filter(user_id=user.id, pk=id).get()
    except:
        raise Http404('Record not found.')

    for field in contact.fillable:
        setattr(contact, field, request.POST.get(field))

    if user.google_credentials and contact.google_id:
        google.delete_contact(contact)
        contact.google_id = google.add_contact(contact)

    contact.save()

    return redirect('contacts')


@login_required
def delete(request, id):
    try:
        contact = Contact.objects.filter(user_id=request.user.id, pk=id).get()
    except:
        raise Http404('Record not found.')
    if contact.google_id:
        google.delete_contact(contact)
    contact.delete()
    return redirect('contacts')


@login_required
def google_sync(request, id):
    contact = get_object_or_404(Contact, pk=id)
    contact.google_id = google.add_contact(contact)
    contact.save()
    return redirect('contacts')
