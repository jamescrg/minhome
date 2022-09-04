
import json
import datetime

from django.shortcuts import get_object_or_404
import google.oauth2.credentials
from apiclient.discovery import build

from accounts.models import CustomUser


def build_service(user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
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


def get_events(user_id):

    service = build_service(user_id)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if events:
        events_simplified = []
        for event in events:
            event_simplified = {}
            start = event['start'].get('dateTime', event['start'].get('date'))
            date = start[0:10]
            datetime_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            weekday = datetime_date.strftime('%A')
            event_simplified['date'] = date
            event_simplified['weekday'] = weekday
            event_simplified['duration'] = start[11:]
            event_simplified['summary'] = event['summary']
            events_simplified.append(event_simplified)
        return events_simplified
    else:
        return None
