
import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.favorites.models import Favorite
from apps.folders.models import Folder


pytestmark = pytest.mark.django_db


def test_favorite_string(favorite):
    favorite = Favorite.objects.get(name="Meditation Posture")
    assert str(favorite) == f'{favorite.name}'


def test_favorite_content(client, user, favorite):
    folder = Folder.objects.all().first()
    favorite = Favorite.objects.get(name='Meditation Posture')
    expectedValues = {
        'user': user,
        'folder_id': folder.id,
        'name': 'Meditation Posture',
        'url': 'http://meditationposture.net',
        'description': 'A website',
        'login': 'drachma',
        'root': 'rupee',
        'passkey': 'ruble',
        'selected': 1,
    }
    for key, val in expectedValues.items():
        assert getattr(favorite, key) == val


def test_index(client):
    response = client.get('/favorites/')
    assert response.status_code == 200
    response = client.get(reverse('favorites'))
    assert response.status_code == 200
    response = client.get(reverse('favorites'))
    assertTemplateUsed(response, 'favorites/content.html')


def test_add(client):
    response = client.get('/favorites/add')
    assert response.status_code == 200
    assertTemplateUsed(response, 'favorites/form.html')


def test_add_data(client, folder1):
    data = {
        'folder': folder1.id,
        'name': 'Reddit',
        'url': 'https://reddit.com',
    }
    response = client.post('/favorites/add', data)
    assert response.status_code == 302
    found = Favorite.objects.filter(name='Reddit').exists()
    assert found


def test_edit(client, favorite):
    response = client.get(f'/favorites/{favorite.id}/edit')
    assert response.status_code == 200
    assertTemplateUsed(response, 'favorites/form.html')


def test_edit_data(client, folder1, favorite):
    data = {
        'folder': folder1.id,
        'name': 'Reddit',
        'url': 'https://reddit.com',
    }
    response = client.post(f'/favorites/{favorite.id}/edit', data)
    assert response.status_code == 302
    found = Favorite.objects.filter(name='Reddit').exists()
    assert found


def test_delete(client, favorite):
    response = client.get(f'/favorites/delete/{favorite.id}')
    assert response.status_code == 302
    found = Favorite.objects.filter(name='Bing').exists()
    assert not found


def test_home(client, favorite):
    response = client.get(f'/favorites/home/{favorite.id}')
    assert response.status_code == 302
    favorite = Favorite.objects.filter(pk=favorite.id).get()
    assert favorite.home_rank == 1
