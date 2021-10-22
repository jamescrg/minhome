
from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

import markdown

from apps.contacts.models import Contact
from apps.contacts.google import add_contact


@login_required
def index(request):

    user_id = request.user.id
    page = 'lab'

    contacts = Contact.objects.filter(user_id=1, id__lt=200).order_by('name')
    count = contacts.count()
    
    for contact in contacts:
        contact.google_id = add_contact(contact)
        contact.save

    context = {
        'page': page,
        'contacts': contacts,
        'count': count,
    }

    return render(request, 'lab/content.html', context)

