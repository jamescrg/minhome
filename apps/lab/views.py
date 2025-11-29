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


@login_required
def sms_test(request):
    """Test SMS functionality by sending a test message."""
    from django.conf import settings

    from config.sms import send_sms

    result = None
    default_message = f"Test SMS from {settings.SITE_NAME}"

    if request.method == "POST":
        recipient = request.POST.get("recipient", "").strip()
        message = request.POST.get("message", "").strip()
        result = send_sms(recipient, message)

    context = {
        "page": "lab",
        "result": result,
        "default_recipient": settings.SMS_RECIPIENT,
        "default_message": default_message,
    }

    return render(request, "lab/sms.html", context)
