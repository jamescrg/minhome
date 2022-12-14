
import pytest

from django.urls import reverse
from django.shortcuts import get_object_or_404
from pytest_django.asserts import assertTemplateUsed

from apps.contacts.models import Folder


pytestmark = pytest.mark.django_db


def test_string(folder):
    folder = Folder.objects.get(name='Main')
    assert str(folder) == f'{folder.name}'


def test_content(user, folder):
    folder = Folder.objects.get(name='Main')
    expectedValues = {
        'user_id': user.id,
        'page': 'favorites',
        'name': 'Main',
        'home_column': 1,
        'home_rank': 1,
        'selected': 1,
        'active': 1,
    }
    for key, val in expectedValues.items():
        assert getattr(folder, key) == val


def test_home(client, folder):
    response = client.get('/folders/home/4/notes')
    assertEqual(response.status_code, 302)
    folder = Folder.objects.filter(pk=4).get()
    assert folder.home_column == 4
    assert folder.home_rank == 1


def test_select(client):
    response = client.get('/folders/4/notes')
    assert response.status_code == 302
    response = client.get('/notes/')
    assert 'Philosophy' in response


def test_insert(client):
    data = {
        'user_id': 1,
        'folder_id': 2,
        'page': 'notes',
        'name': 'Existentialism',
    }

    response = client.post('/folders/insert/notes', data)
    assert response.status_code == 302
    found = Folder.objects.filter(name='Existentialism').exists()
    assert found


def test_update(client):
    data = {
        'user_id': user.id,
        'folder_id': 4,
        'page': 'notes',
        'name': 'Existentialism',
    }

    response = client.post('/folders/update/4/notes', data)
    assert response.status_code == 302
    found = Folder.objects.filter(name='Existentialism').exists()
    assert found


def test_delete(client):
    response = client.get('/folders/delete/4/notes')
    found = Folder.objects.filter(name='Philosophy').exists()
    assert not found
