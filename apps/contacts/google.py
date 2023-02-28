import json

import google.oauth2.credentials
from apiclient.discovery import build
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser


def build_service(contact):
    """Create an instance of the Google API service.

    Args:
        contact (Contact): an instance of the Contact model

    Returns:
        service (??): a Google service object of some kind

    Notes:
        A contact is passed into this function to identify the
        user associated with that contact.  Then, with that information,
        the function can locate the user's Google credentials. Then the function
        has the information it needs to build the Google service object

    """

    user = get_object_or_404(CustomUser, pk=contact.user.id)
    credentials = user.google_credentials

    if credentials:
        credentials = json.loads(credentials)
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            credentials
        )
        service = build("people", "v1", credentials=credentials)
        return service
    else:
        return False


def add_contact(contact):
    """Add a contact to the user's Google account.

    Args:
        contact (Contact): an instance of the Contact model

    Returns:
        google_id (str): a unique identifier associated with the Google contact

    Notes:
        Attempts to add a user's contact to their Google account. If successful, returns
        the unique identifier associated with the Google contact that was added.
        If unsuccessful, returns false.

    """

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
            google_id = result["resourceName"]
            return google_id
        else:
            return False

    else:
        return False


def delete_contact(contact):
    """Delete a contact from the user's Google account.

    Args:
        contact (Contact): the contact to be deleted

    Returns:
        True/False

    Notes:
        Attempts to delete a user's contact from their Google account.
        If successful, returns True, otherwise returns False.

    """
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
