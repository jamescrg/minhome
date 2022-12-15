
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
        'home_column': 0,
        'home_rank': 0,
        'selected': 0,
        'active': 0,
    }
    for key, val in expectedValues.items():
        assert getattr(folder, key) == val


def test_home(client, folder):
    response = client.get(f'/folders/home/{folder.id}/notes')
    assert response.status_code == 302
    folder = Folder.objects.filter(pk=folder.id).get()
    assert folder.home_column == 4
    assert folder.home_rank == 1


def test_select(client, folders):
    folder = Folder.objects.filter(name='Philosophy').get()
    response = client.get(f'/folders/{folder.id}/notes')
    assert response.status_code == 302
    response = client.get('/notes/')
    assert folder in response.context['folders']


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


def test_update(client, folder):
    data = {
        'name': 'Atlanta',
    }
    response = client.post(f'/folders/update/{folder.id}/favorites', data)
    assert response.status_code == 302
    found = Folder.objects.filter(name='Atlanta').exists()
    assert found


def test_delete(client, folder):
    client.get(f'/folders/delete/{folder.id}/notes')
    found = Folder.objects.filter(id=folder.id).exists()
    assert not found
