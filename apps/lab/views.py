
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.contacts.models import Contact


@login_required
def index(request):
    from django.http import Http404, HttpResponse
    raise Http404('bad link')
    return HttpResponse('this is the response')


@login_required
def email_test(request):
    """Test whether I can send an email

    """
    from django.core.mail import send_mail
    from config import settings_local

    send_mail(
        'Test Message',
        'This is the message body.',
        settings_local.SERVER_EMAIL,
        settings_local.TEST_EMAIL_RECIPIENT,
        fail_silently=False,
    )

    page = 'lab'

    context = {
        'page': page,
    }

    return render(request, 'lab/content.html', context)
