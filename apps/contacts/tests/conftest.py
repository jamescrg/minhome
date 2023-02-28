import pytest
from django.test import Client

from accounts.models import CustomUser
from apps.contacts.models import Contact
from apps.folders.models import Folder


@pytest.fixture
def user():
    user = CustomUser.objects.create_user("Ollie", "ollie@gmail.com", "clawboy")
    return user


@pytest.fixture
def folder1(user):
    folder1 = Folder.objects.create(
        user=user,
        page="contacts",
        name="Mahatmas",
    )
    folder1.save()
    return folder1


@pytest.fixture
def client(user):
    client = Client()
    client.login(username="Ollie", password="clawboy")
    return client


@pytest.fixture
def contact(user, folder1):
    contact = Contact.objects.create(
        user=user,
        folder=folder1,
        selected=0,
        name="Mohandas Gandhi",
        company="Gandhi, PC",
        address="225 Paper Street, Porbandar, India",
        phone1="123.456.7890",
        phone1_label="Work",
        phone2="123.456.2222",
        phone2_label="Mobile",
        phone3="123.456.5555",
        phone3_label="Other",
        email="gandhi@gandhi.com",
        website="gandhi.com",
        notes="The Mahatma",
    )
    contact.save()
    return contact


@pytest.fixture
def contact_data(contact):
    contact_data = contact.__dict__
    keys = "_state id folder_id google_id".split()
    for key in keys:
        del contact_data[key]
    return contact_data
