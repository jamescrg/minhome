
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
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
