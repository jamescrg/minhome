import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import apps.contacts.google as google
from apps.contacts.forms import ContactForm
from apps.contacts.models import Contact
from apps.folders.folders import get_folder_tree, select_folder
from apps.folders.models import Folder


@login_required
def index(request):
    """Display a list of folders and contacts, along with a contact.

    Notes:
        Always displays folders.
        If a folder is selected, displays the contacts for a folder.
        If a contact is selected, displays the contact.

    """

    selected_folder = select_folder(request, "contacts")

    # Get folder tree starting from selected folder
    folder_tree, tree_has_children = get_folder_tree(
        request, "contacts", selected_folder
    )

    if selected_folder:
        # Get contacts from selected folder only
        contacts = Contact.objects.filter(user=request.user, folder=selected_folder)
    else:
        contacts = Contact.objects.filter(user=request.user, folder_id__isnull=True)

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
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
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
    return redirect("contacts")


@login_required
def add(request):
    """Add a new contact.

    Notes:
        GET: Display new contact form.
        POST: Add contact to database.

    """
    user = request.user
    selected_folder = select_folder(request, "contacts")

    folder_tree, tree_has_children = get_folder_tree(
        request, "contacts", selected_folder
    )

    # if applicable, process any post data submitted by user
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # initialize contact data
            contact = form.save(commit=False)
            contact.user = user
            contact.folder = selected_folder  # Always assign to selected folder

            # save contact to database
            contact.save()

            # Update user's selected contact to the newly created contact
            user.contacts_contact = contact.id
            user.save()

            return redirect("contacts")

    # if no post data has been submitted, show the contact form
    else:
        form = ContactForm()

    context = {
        "page": "contacts",
        "edit": False,
        "add": True,
        "action": "/contacts/add",
        "folder_tree": folder_tree,
        "tree_has_children": tree_has_children,
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

    selected_folder = select_folder(request, "contacts")

    folder_tree, tree_has_children = get_folder_tree(
        request, "contacts", selected_folder
    )

    contact = get_object_or_404(Contact, pk=id)

    if request.method == "POST":
        try:
            contact = Contact.objects.filter(user=user, pk=id).get()
        except ObjectDoesNotExist:
            raise Http404("Record not found.")

        form = ContactForm(request.POST, instance=contact)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = user

            if user.google_credentials and contact.google_id:
                google.delete_contact(contact)
                contact.google_id = google.add_contact(contact)

            contact.save()

            return redirect("contacts")

    else:
        form = ContactForm(instance=contact)

        context = {
            "page": "contacts",
            "edit": True,
            "add": False,
            "action": f"/contacts/{id}/edit",
            "folder_tree": folder_tree,
            "tree_has_children": tree_has_children,
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


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def move_to_folder(request):
    """Move a contact to a different folder.

    Expected POST data:
        item_id: ID of the contact to move
        folder_id: ID of the target folder
    """
    try:
        data = json.loads(request.body)
        item_id = data.get("item_id")
        folder_id = data.get("folder_id")

        if not item_id or not folder_id:
            return JsonResponse(
                {"success": False, "message": "Missing required parameters"}
            )

        # Get the contact
        contact = get_object_or_404(Contact, pk=item_id, user=request.user)

        # Get the target folder
        folder = get_object_or_404(Folder, pk=folder_id, user=request.user)

        # Move the contact to the new folder
        contact.folder = folder
        contact.save()

        return JsonResponse({"success": True, "message": "Contact moved successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON data"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
