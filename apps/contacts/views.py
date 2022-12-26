
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.folders.folders import select_folders
from apps.contacts.models import Contact
from apps.contacts.forms import ContactForm
import apps.contacts.google as google


@login_required
def index(request):

    folders = Folder.objects.filter(user=request.user, page='contacts').order_by('name')

    selected_folder = select_folders(request, 'contacts')

    if selected_folder:
        contacts = Contact.objects.filter(user=request.user, folder=selected_folder)
    else:
        contacts = Contact.objects.filter(user=request.user, folder_id__isnull=True)

    contacts = contacts.order_by('name')

    selected_contact = Contact.objects.filter(user=request.user, selected=1).first()

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
    user = request.user
    Contact.objects.filter(user=user, selected=1).update(selected=0)
    new = get_object_or_404(Contact, pk=id)
    new.selected = 1
    new.save()
    return redirect('/contacts/')


@login_required
def add(request):

    # load initial page values (user, folders, selected folder)
    user = request.user
    folders = Folder.objects.filter(user=user, page='contacts').order_by('name')

    selected_folder = select_folders(request, 'contacts')

    # if applicable, process any post data submitted by user
    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():

            # initialize contact data
            contact = form.save(commit=False)
            contact.user = user

            # add to google account
            if user.google_credentials:
                contact.google_id = google.add_contact(contact)

            # save contact to database with google id
            contact.save()

            # deselect previously selected contact, if one exists
            try:
                old = Contact.objects.filter(user=user, selected=1).get()
            except Contact.DoesNotExist:
                pass
            else:
                old.selected = 0
                old.save()

            # select newest contact for user
            new = Contact.objects.filter(user=user).latest('id')
            new.selected = 1
            new.save()

            return redirect('contacts')

    # if no post data has been submitted, show the contact form
    else:

        if selected_folder:
            form = ContactForm(initial={'folder': selected_folder.id})
        else:
            form = ContactForm()

    form.fields['folder'].queryset = Folder.objects.filter(
        user=user, page='contacts').order_by('name')

    context = {
        'page': 'contacts',
        'edit': False,
        'add': True,
        'action': '/contacts/add',
        'folders': folders,
        'form': form,
        'phone_labels': ['Mobile', 'Home', 'Work', 'Fax', 'Other'],
    }

    return render(request, 'contacts/content.html', context)


@login_required
def edit(request, id):

    user = request.user
    folders = Folder.objects.filter(user=user, page='contacts').order_by('name')

    selected_folder = select_folders(request, 'contacts')

    contact = get_object_or_404(Contact, pk=id)

    if request.method == 'POST':

        try:
            contact = Contact.objects.filter(user=user, pk=id).get()
        except ObjectDoesNotExist:
            raise Http404('Record not found.')

        form = ContactForm(request.POST, instance=contact)
        form.fields['folder'].queryset = Folder.objects.filter(
            user=user, page='contacts').order_by('name')

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = user

            if user.google_credentials and contact.google_id:
                google.delete_contact(contact)
                contact.google_id = google.add_contact(contact)

            contact.save()

            return redirect('contacts')

    else:

        if selected_folder:
            form = ContactForm(instance=contact, initial={'folder': selected_folder.id})
        else:
            form = ContactForm(instance=contact)

    form.fields['folder'].queryset = Folder.objects.filter(
        user=user, page='contacts').order_by('name')

    context = {
        'page': 'contacts',
        'edit': True,
        'add': False,
        'action': f'/contacts/{id}/edit',
        'folders': folders,
        'selected_folder': selected_folder,
        'contact': contact,
        'form': form,
    }

    return render(request, 'contacts/content.html', context)


@login_required
def delete(request, id):
    try:
        contact = Contact.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
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
