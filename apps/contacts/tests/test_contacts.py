
import pytest

from django.urls import reverse
from django.shortcuts import get_object_or_404
from pytest_django.asserts import assertTemplateUsed

from apps.contacts.models import Contact

# This flags all tests in the file as needing database access
# Once setup, the database is cached to be used for all subsequent tests
# and rolls back transactions, to isolate tests from each other.
# This is the same way the standard Django TestCase uses the database.
# However pytest-django also caters for transaction test cases and allows you to
# keep the test databases configured across different test runs.
pytestmark = pytest.mark.django_db


def test_contact_string(contact):
    contact = Contact.objects.get(name='Mohandas Gandhi')
    assert str(contact) == f'{contact.name} : {contact.id}'


def test_contact_content(contact):
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


def test_select(client, user, folder1, contact):
    response = client.get(f'/contacts/{contact.id}')
    assert response.status_code == 302
    selected_contact = get_object_or_404(Contact, pk=contact.id)
    assert selected_contact.selected == 1


def test_add(client):
    response = client.get('/contacts/add')
    assert response.status_code == 200
    assertTemplateUsed(response, 'contacts/form.html')


def test_add_data(client, folder1):
    data = {
        'folder': folder1.id,
        'name': 'Plato',
        'phone1': '440.500.6000',
    }
    response = client.post('/contacts/add', data)
    assert response.status_code == 302
    found = Contact.objects.filter(name='Plato').exists()
    assert found


def test_edit(client, contact):
    response = client.get(f'/contacts/{contact.id}/edit')
    assert response.status_code == 200
    assertTemplateUsed(response, 'contacts/form.html')


def test_edit_data(client, folder1, contact):
    data = {
        'folder': folder1.id,
        'name': 'Descartes',
        'phone1': '440.500.6000',
    }
    response = client.post(f'/contacts/{contact.id}/edit', data)
    assert response.status_code == 302
    found = Contact.objects.filter(name='Descartes').exists()
    assert found


def test_delete(client, contact):
    response = client.get(f'/contacts/{contact.id}/delete')
    assert response.status_code == 302
    found = Contact.objects.filter(name='Schopenhauer').exists()
    assert not found
