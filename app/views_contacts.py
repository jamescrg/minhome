from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Folder, Contact
from pprint import pprint

@login_required
def index(request):

    user_id = request.user.id
    page = 'contacts'

    folders = Folder.objects.filter(user_id=user_id, page=page).order_by('name')

    selected_folder = Folder.objects.filter(user_id=user_id, 
            page=page, selected=1).first()
   
    if selected_folder:
        contacts = Contact.objects.filter(user_id=user_id, folder_id=selected_folder.id)
    else:
        contacts = Contact.objects.filter(user_id=user_id, folder_id=0)
    contacts = contacts.order_by('name')

    selected_contact = Contact.objects.filter(user_id=user_id, selected=1).get()

    context = {
        'page': 'contacts',
        'edit': False,
        'folders': folders,
        'selected_folder': selected_folder,
        'contacts': contacts,
        'selected_contact': selected_contact,
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
def create(request, id):
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



