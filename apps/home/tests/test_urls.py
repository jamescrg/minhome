

import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


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
