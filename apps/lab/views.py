
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.contacts.models import Contact


@login_required
def index(request):

    user = request.user
    page = 'lab'

    contacts = Contact.objects.filter(user=user, google_id__isnull=True).order_by('name')[:10]
    count = contacts.count()

    # for contact in contacts:
    #     contact.google_id = add_contact(contact)
    #     contact.save()

    context = {
        'page': page,
        'contacts': contacts,
        'count': count,
    }

    return render(request, 'lab/content.html', context)

