"""Email utility for task reminders."""

import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_task_reminder_email(user, task, reminder_type):
    """Send a task reminder email.

    Args:
        user: CustomUser instance
        task: Task instance
        reminder_type: "due_today", "due_soon", or "overdue"

    Returns:
        dict with 'success' boolean and optional 'error'
    """
    if not user.email:
        return {"success": False, "error": "User has no email address"}

    subject_map = {
        "due_today": f"Task Due Today: {task.title}",
        "due_soon": f"Task Due Soon: {task.title}",
        "overdue": f"Overdue Task: {task.title}",
    }
    subject = subject_map.get(reminder_type, f"Task Reminder: {task.title}")

    body = _build_body(task, reminder_type)

    try:
        send_mail(
            subject, body, settings.SERVER_EMAIL, [user.email], fail_silently=False
        )
        logger.info(
            f"Reminder sent to {user.email} for task {task.id} ({reminder_type})"
        )
        return {"success": True}
    except Exception as e:
        logger.error(f"Failed to send reminder to {user.email} for task {task.id}: {e}")
        return {"success": False, "error": str(e)}


def _build_body(task, reminder_type):
    """Build plain text email body."""
    lines = []
    if reminder_type == "due_today":
        lines.append(f'Your task "{task.title}" is due today.')
    elif reminder_type == "due_soon":
        time_str = task.due_time.strftime("%-I:%M %p") if task.due_time else ""
        lines.append(f'Your task "{task.title}" is due soon at {time_str}.')
    elif reminder_type == "overdue":
        lines.append(f'Your task "{task.title}" is overdue.')

    lines.append("")
    if task.due_date:
        lines.append(f"Due date: {task.due_date.strftime('%B %-d, %Y')}")
    if task.due_time:
        lines.append(f"Due time: {task.due_time.strftime('%-I:%M %p')}")
    if task.folder:
        lines.append(f"Folder: {task.folder.name}")
    lines.append("")
    lines.append(f"-- {settings.SITE_NAME}")
    return "\n".join(lines)
