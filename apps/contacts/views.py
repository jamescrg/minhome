from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

import apps.contacts.google as google
from apps.contacts.forms import ContactForm
from apps.contacts.models import Contact
from apps.folders.folders import select_folder
from apps.folders.models import Folder


@login_required
def index(request):
    """Display a list of folders and contacts, along with a contact.

    Notes:
        Always displays folders.
        If a folder is selected, displays the contacts for a folder.
        If a contact is selected, displays the contact.

    """

    folders = Folder.objects.filter(
        user=request.user, page="contacts").order_by("name")

    selected_folder = select_folder(request, "contacts")

    if selected_folder:
        contacts = Contact.objects.filter(
            user=request.user, folder=selected_folder)
    else:
        contacts = Contact.objects.filter(
            user=request.user, folder_id__isnull=True)

    contacts = contacts.order_by("name")

    selected_contact_id = request.user.contacts_contact

    try:
        selected_contact = Contact.objects.filter(pk=selected_contact_id).get()
    except ObjectDoesNotExist:
        selected_contact = None

    if request.user.google_credentials:
        google = True
    else:
        google = False

    context = {
        "page": "contacts",
        "edit": False,
        "folders": folders,
        "selected_folder": selected_folder,
        "contacts": contacts,
        "selected_contact": selected_contact,
        "google": google,
    }

    return render(request, "contacts/content.html", context)


@login_required
def select(request, id):
    """Select a contact for display, redirect to index.

    Args:
        id (int): a Contact instance id

    """

    user = request.user
    user.contacts_contact = id
    user.save()
    return redirect("/contacts/")


@login_required
def add(request):
    """Add a new contact.

    Notes:
        GET: Display new contact form.
        POST: Add contact to database.

    """

    # load initial page values (user, folders, selected folder)
    user = request.user
    folders = Folder.objects.filter(user=user, page="contacts").order_by("name")

    selected_folder = select_folder(request, "contacts")

    # if applicable, process any post data submitted by user
    if request.method == "POST":
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
            new = Contact.objects.filter(user=user).latest("id")
            new.selected = 1
            new.save()

            return redirect("contacts")

    # if no post data has been submitted, show the contact form
    else:
        if selected_folder:
            form = ContactForm(initial={"folder": selected_folder.id})
        else:
            form = ContactForm()

    form.fields["folder"].queryset = Folder.objects.filter(
        user=user, page="contacts"
    ).order_by("name")

    context = {
        "page": "contacts",
        "edit": False,
        "add": True,
        "action": "/contacts/add",
        "folders": folders,
        "form": form,
        "phone_labels": ["Mobile", "Home", "Work", "Fax", "Other"],
    }

    return render(request, "contacts/content.html", context)


@login_required
def edit(request, id):
    """Edit a contact.

    Args:
        id (int): A Contact instance id

    Notes:
        GET: Display contact form.
        POST: Update contact in database.

    """

    user = request.user
    folders = Folder.objects.filter(user=user, page="contacts").order_by("name")

    selected_folder = select_folder(request, "contacts")

    contact = get_object_or_404(Contact, pk=id)

    if request.method == "POST":
        try:
            contact = Contact.objects.filter(user=user, pk=id).get()
        except ObjectDoesNotExist:
            raise Http404("Record not found.")

        form = ContactForm(request.POST, instance=contact)
        form.fields["folder"].queryset = Folder.objects.filter(
            user=user, page="contacts"
        ).order_by("name")

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = user

            if user.google_credentials and contact.google_id:
                google.delete_contact(contact)
                contact.google_id = google.add_contact(contact)

            contact.save()

            return redirect("contacts")

    else:
        if selected_folder:
            form = ContactForm(instance=contact, initial={"folder": selected_folder.id})
        else:
            form = ContactForm(instance=contact)

    form.fields["folder"].queryset = Folder.objects.filter(
        user=user, page="contacts"
    ).order_by("name")

    context = {
        "page": "contacts",
        "edit": True,
        "add": False,
        "action": f"/contacts/{id}/edit",
        "folders": folders,
        "selected_folder": selected_folder,
        "contact": contact,
        "form": form,
    }

    return render(request, "contacts/content.html", context)


@login_required
def delete(request, id):
    """Delete a contact.

    Args:
        id (int):  a Contact instance id

    """

    try:
        contact = Contact.objects.filter(user=request.user, pk=id).get()
    except ObjectDoesNotExist:
        raise Http404("Record not found.")
    if contact.google_id:
        google.delete_contact(contact)
    contact.delete()
    return redirect("contacts")


@login_required
def google_toggle(request, id):
    """Add a contact to Google account, update the contact with its google_id.

    Args:
        id (int): a Contact instance id

    Notes:
        Invoked by a link under the contact,
        which is displayed if the contact does not have a google_id.

    """

    contact = get_object_or_404(Contact, pk=id)
    if contact.google_id:
        google.delete_contact(contact)
        contact.google_id = ""
    else:
        contact.google_id = google.add_contact(contact)

    contact.save()
    return redirect("contacts")


@login_required
def google_list(request):

    contacts = Contact.objects.all()
    # for contact in contacts:
    #     contact.google_id = ""
    #     contact.save()

    context = {
        "page": "contacts",
        "contacts": contacts,
    }

    return render(request, "contacts/google.html", context)


