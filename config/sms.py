"""
SMS Service Module using Twilio

Provides functions to send SMS messages for:
- Task reminders
- Manual/on-demand messages
- System alerts
"""

import logging

from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


def get_client():
    """Get configured Twilio client."""
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        raise ValueError("Twilio credentials not configured")
    return Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_sms(to, body):
    """
    Send an SMS message.

    Args:
        to: Phone number to send to (E.164 format, e.g., +1234567890)
        body: Message content (max 1600 characters)

    Returns:
        dict with 'success' boolean and 'message_sid' or 'error'
    """
    if not to:
        return {"success": False, "error": "No recipient phone number provided"}

    if not body:
        return {"success": False, "error": "No message body provided"}

    try:
        client = get_client()
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to,
        )
        logger.info(f"SMS sent successfully: {message.sid}")
        return {"success": True, "message_sid": message.sid}

    except TwilioRestException as e:
        logger.error(f"Twilio error: {e}")
        return {"success": False, "error": str(e)}

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return {"success": False, "error": str(e)}


def send_task_reminder(to, task_title, due_date=None, due_time=None):
    """
    Send a task reminder SMS.

    Args:
        to: Phone number
        task_title: Name of the task
        due_date: Optional due date
        due_time: Optional due time
    """
    body = f"Task Reminder: {task_title}"
    if due_date:
        body += f"\nDue: {due_date}"
        if due_time:
            body += f" at {due_time}"
    return send_sms(to, body)


def send_alert(to, alert_type, message):
    """
    Send a system alert SMS.

    Args:
        to: Phone number
        alert_type: Type of alert (e.g., 'ERROR', 'WARNING', 'INFO')
        message: Alert message
    """
    body = f"[{alert_type}] {settings.SITE_NAME}: {message}"
    return send_sms(to, body)


def send_to_admin(body):
    """
    Send SMS to the configured admin recipient.

    Uses SMS_RECIPIENT from settings.
    """
    return send_sms(settings.SMS_RECIPIENT, body)
