

import pytest
import random

from apps.favorites.models import Favorite

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


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

