import pytest

from apps.contacts.models import Contact


pytestmark = pytest.mark.django_db


def test_contact_string(contact):
    contact = Contact.objects.get(name="Mohandas Gandhi")
    assert str(contact) == f"{contact.name} : {contact.id}"


def test_contact_content(contact):
    contact = Contact.objects.get(name="Mohandas Gandhi")
    expectedValues = {
        "name": "Mohandas Gandhi",
        "company": "Gandhi, PC",
        "address": "225 Paper Street, Porbandar, India",
        "phone1": "123.456.7890",
        "phone1_label": "Work",
        "phone2": "123.456.2222",
        "phone2_label": "Mobile",
        "phone3": "123.456.5555",
        "phone3_label": "Other",
        "email": "gandhi@gandhi.com",
        "notes": "The Mahatma",
    }
    for key, val in expectedValues.items():
        assert getattr(contact, key) == val
