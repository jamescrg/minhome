from pprint import pprint
import json

from django.shortcuts import get_object_or_404
import google.oauth2.credentials
import google_auth_oauthlib.flow
from apiclient.discovery import build

from accounts.models import CustomUser
from apps.contacts.models import Contact


def build_service(contact):
    user = get_object_or_404(CustomUser, pk=contact.user_id)
    credentials = user.google_credentials

    if credentials:
        credentials = json.loads(credentials)
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            credentials
        )
        service = build('people', 'v1', credentials=credentials)
        return service
    else:
        return False


def add_contact(contact):
    service = build_service(contact)

    if service:
        new_contact = {
            "names": [{"unstructuredName": contact.name}],
            "emailAddresses": [{"value": contact.email}],
            "phoneNumbers": [
                {
                    "value": contact.phone1,
                    "type": contact.phone1_label,
                },
                {
                    "value": contact.phone2,
                    "type": contact.phone2_label,
                },
                {
                    "value": contact.phone3,
                    "type": contact.phone3_label,
                },
            ],
        }

        result = service.people().createContact(body=new_contact).execute()

        if result:
            google_id = result['resourceName']
            return google_id
        else:
            return False

    else:
        return False


def delete_contact(contact):
    service = build_service(contact)

    if service:
        result = (
            service.people().deleteContact(resourceName=contact.google_id).execute()
        )

        if result:
            return True
        else:
            return False

    else:
        return False
