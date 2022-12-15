
import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.favorites.models import Favorite
from apps.folders.models import Folder


pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


# ------------------------------------
# urls and templates
# ------------------------------------

def test_base_url(client):
    response = client.get('/')
    assert response.status_code == 200


def test_home_url(client):
    response = client.get('/home/')
    assert response.status_code == 200


def test_named_route(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200


def test_correct_template(client):
    response = client.get(reverse('home'))
    assertTemplateUsed(response, 'home/index.html')


# ------------------------------------
# folder movement
# ------------------------------------

def test_redirect(client, folders):
    response = client.get(f'/home/folder/{folders[3].id}/up/')
    assert response.status_code == 302


def test_up_from_bottom(client, folders):
    client.get(f'/home/folder/{folders[3].id}/up/')
    folder = Folder.objects.get(pk=folders[3].id)
    assert folder.home_rank == 3
    folder = Folder.objects.get(pk=folders[2].id)
    assert folder.home_rank == 4


def test_up_from_middle(client, folders):
    client.get(f'/home/folder/{folders[2].id}/up/')
    folder = Folder.objects.get(pk=3)
    assert folder.home_rank == 2


def test_up_from_top(client, folders):
    client.get(f'/home/folder/{folders[0].id}/up/')
    folder = Folder.objects.get(pk=folders[0].id)
    assert folder.home_rank == 1
    folder = Folder.objects.get(pk=folders[1].id)
    assert folder.home_rank == 2


def test_down_from_bottom(client, folders):
    client.get(f'/home/folder/{folders[15].id}/down/')
    folder = Folder.objects.get(pk=folders[15].id)
    assert folder.home_rank == 4
    folder = Folder.objects.get(pk=folders[14].id)
    assert folder.home_rank == 3


def test_down_from_middle(client, folders):
    client.get(f'/home/folder/{folders[9].id}/down/')
    folder = Folder.objects.get(pk=folders[9].id)
    assert folder.home_rank == 3
    folder = Folder.objects.get(pk=folders[10].id)
    assert folder.home_rank == 2


def test_down_from_top(client, folders):
    client.get(f'/home/folder/{folders[12].id}/down/')
    folder = Folder.objects.get(pk=folders[12].id)
    assert folder.home_rank == 2
    folder = Folder.objects.get(pk=folders[13].id)
    assert folder.home_rank == 1


def test_down_from_top_to_bottom(client, folders):
    client.get(f'/home/folder/{folders[0].id}/down/')
    client.get(f'/home/folder/{folders[0].id}/down/')
    client.get(f'/home/folder/{folders[0].id}/down/')
    folder = Folder.objects.get(pk=folders[0].id)
    assert folder.home_rank == 4
    folder = Folder.objects.get(pk=folders[3].id)
    assert folder.home_rank == 3


def test_left_from_far_left(client, folders):
    client.get(f'/home/folder/{folders[0].id}/left/')
    folder = Folder.objects.get(pk=folders[0].id)
    assert folder.home_column == 1


def test_left_from_middle_left(client, folders):
    client.get(f'/home/folder/{folders[4].id}/left/')
    folder = Folder.objects.get(pk=folders[4].id)
    assert folder.home_column == 1
    assert folder.home_rank == 5


def test_right_from_middle_right(client, folders):
    client.get(f'/home/folder/{folders[8].id}/right/')
    folder = Folder.objects.get(pk=folders[8].id)
    assert folder.home_column == 4
    assert folder.home_rank == 5


def test_right_from_far_right(client, folders):
    client.get(f'/home/folder/{folders[12].id}/right/')
    folder = Folder.objects.get(pk=folders[12].id)
    assert folder.home_column == 4


# ------------------------------------
# favorite movement
# ------------------------------------

def test_favorite_up_from_bottom(client, favorites):
    client.get(f'/home/favorite/{favorites[4].id}/up/')
    favorite = Favorite.objects.get(pk=favorites[4].id)
    assert favorite.home_rank == 4
    favorite = Favorite.objects.get(pk=favorites[3].id)
    assert favorite.home_rank == 5


def test_favorite_up_from_top(client, favorites):
    client.get(f'/home/favorite/{favorites[0].id}/up/')
    favorite = Favorite.objects.get(pk=favorites[0].id)
    assert favorite.home_rank == 1


def test_favorite_down_from_bottom(client, favorites):
    client.get(f'/home/favorite/{favorites[4].id}/down/')
    favorite = Favorite.objects.get(pk=favorites[4].id)
    assert favorite.home_rank == 6


def test_favorite_down_from_top(client, favorites):
    client.get(f'/home/favorite/{favorites[0].id}/down/')
    favorite = Favorite.objects.get(pk=favorites[0].id)
    assert favorite.home_rank == 2
    favorite = Favorite.objects.get(pk=favorites[1].id)
    assert favorite.home_rank == 1


