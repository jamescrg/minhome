
from pprint import pprint
import pytest

from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from pytest_django.asserts import assertTemplateUsed, assertContains

from accounts.models import CustomUser
import apps.finance.crypto_data as crypto_data

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def user():
    user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username='john', password='johnpassword')
    return client



# ---------------------------------------------------------------------------
# tests
# ---------------------------------------------------------------------------


def test_crypto(client):
    response = client.get('/crypto/')
    assert response.status_code == 200
    assert response.context['page'] == 'crypto'
    assert 'market_cap' in response.context['data'][0]
    assertTemplateUsed(response, 'finance/crypto.html')
    assertContains(response, 'BTC')
    assertContains(response, 'Bitcoin')
    assertContains(response, '24h Chg')


def test_securities(client):
    response = client.get('/securities/')
    assert response.status_code == 200
    assert response.context['page'] == 'securities'
    assert response.context['data'][0]['price'] > 0
    assertTemplateUsed(response, 'finance/securities.html')


def test_positions(client):
    response = client.get('/positions/')
    assert response.status_code == 200
    response = client.get(reverse('positions'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'finance/positions.html')
