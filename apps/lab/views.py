from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    count = 7
    context = {
        "count": count,
    }
    return render(request, "lab/content.html", context)


@login_required
def email_test(request):
    """Test whether I can send an email"""
    from django.core.mail import send_mail

    from config import settings_local

    send_mail(
        "Test Message",
        "This is the message body.",
        settings_local.SERVER_EMAIL,
        settings_local.TEST_EMAIL_RECIPIENT,
        fail_silently=False,
    )

    page = "lab"

    context = {
        "page": page,
    }

    return render(request, "lab/content.html", context)
