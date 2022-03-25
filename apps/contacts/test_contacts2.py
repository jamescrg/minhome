
import pytest
from accounts.models import CustomUser

from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from pytest_django.asserts import assertTemplateUsed

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.contacts.models import Contact

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    user = CustomUser.objects.create_user(
        'john', 'lennon@thebeatles.com', 'johnpassword'
    )
    return user


@pytest.fixture
def folder1(user):
    folder1 = Folder.objects.create(
        user=user,
        page='contacts',
        name='mahatmas',
    )
    return folder1


@pytest.fixture
def contact(user, folder1):
    Contact.objects.create(
        user=user,
        folder=folder1,
        selected=1,
        name='Mohandas Gandhi',
        company='Gandhi, PC',
        address='225 Paper Street, Porbandar, India',
        phone1='123.456.7890',
        phone1_label='Work',
        phone2='123.456.2222',
        phone2_label='Mobile',
        phone3='123.456.5555',
        phone3_label='Other',
        email='gandhi@gandhi.com',
        website='gandhi.com',
        notes='The Mahatma',
    )


@pytest.fixture
def client(user):
    client = Client()
    client.login(username='john', password='johnpassword')
    return client


def test_contact_string(user, folder1, contact):
    contact = Contact.objects.get(name='Mohandas Gandhi')
    assert str(contact) == f'{contact.name} : {contact.id}'


def test_contact_content(user, folder1, contact):
    contact = Contact.objects.get(name='Mohandas Gandhi')
    expectedValues = {
        'name': 'Mohandas Gandhi',
        'company': 'Gandhi, PC',
        'address': '225 Paper Street, Porbandar, India',
        'phone1': '123.456.7890',
        'phone1_label': 'Work',
        'phone2': '123.456.2222',
        'phone2_label': 'Mobile',
        'phone3': '123.456.5555',
        'phone3_label': 'Other',
        'email': 'gandhi@gandhi.com',
        'website': 'gandhi.com',
        'notes': 'The Mahatma',
    }
    for key, val in expectedValues.items():
        assert getattr(contact, key) == val


def test_index(client):
    response = client.get('/contacts/')
    assert response.status_code == 200
    response = client.get(reverse('contacts'))
    assert response.status_code == 200
    response = client.get(reverse('contacts'))
    assertTemplateUsed(response, 'contacts/content.html')
