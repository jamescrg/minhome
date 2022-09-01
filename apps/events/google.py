import json
from datetime import timedelta

from django.shortcuts import get_object_or_404
import google.oauth2.credentials
from apiclient.discovery import build

from accounts.models import CustomUser


def build_service(event):
    user = get_object_or_404(CustomUser, pk=event.user_id)
    credentials = user.google_credentials

    if credentials:
        credentials = json.loads(credentials)
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            credentials
        )
        service = build('calendar', 'v3', credentials=credentials)
        return service
    else:
        return False


def add_event(event):

    service = build_service(event)

    if service:
        new_event = {
            'summary': f'{event.description}',
            'start': {
                'date': str(event.date),
                'timezone': 'US/Eastern',
            },
            'end': {
                'date': str(event.date + timedelta(days=1)),
                'timezone': 'US/Eastern',
            },
        }

        google_event = (
            service.events().insert(calendarId='primary', body=new_event).execute()
        )

        if google_event:
            google_id = google_event.get('id')
            return google_id
        else:
            return None

    else:
        return None


def delete_event(event):

    service = build_service(event)

    if service:
        result = (
            service.events()
            .delete(
                calendarId='primary',
                eventId=event.google_id,
            )
            .execute()
        )

        if result:
            return True
        else:
            return False

    else:
        return False


def edit_event(event):

    service = build_service(event)

    if service:
        revised_event = {
            'summary': f'{event.description}',
            'start': {
                'date': str(event.date),
            },
            'end': {
                'date': str(event.date + timedelta(days=1)),
            },
        }

        result = (
            service.events()
            .update(
                calendarId='primary',
                eventId=event.google_id,
                body=revised_event,
            )
            .execute()
        )

        if result:
            return True
        else:
            return False

    else:
        return False
