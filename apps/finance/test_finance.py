
from pprint import pprint
import pytest

from django.test import Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from pytest_django.asserts import assertTemplateUsed, assertContains

from accounts.models import CustomUser
import apps.finance.crypto_data as crypto_data

pytestmark = pytest.mark.django_db


# -------------------------------------------
# fixtures
# -------------------------------------------

@pytest.fixture
def user():
    user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username='john', password='johnpassword')
    return client



# -------------------------------------------
# tests
# -------------------------------------------

def test_crypto_symbols():

    positions = {
        'BTC': 0.7903,
        'ETH': 12,
    }
    symbols = crypto_data.symbols(positions)
    assert symbols == 'BTC,ETH'

    positions.update({
        'IMX': 3500,
        'MATIC': 3000,
    })
    symbols = crypto_data.symbols(positions)
    assert symbols == 'BTC,ETH,IMX,MATIC'


def test_crypto_fetch():
    symbols = 'BTC'
    data = crypto_data.fetch(symbols)
    for key, val in data.items():
        data[key] = data[key]['quote']['USD']
    pprint(data)
    assert data is True


def test_crypto_view(client):
    response = client.get('/crypto/')
    assert response.status_code == 200
    assert response.context['page'] == 'crypto'
    assert response.context['crypto_data'][0]['max_supply'] == 21000000
    assertTemplateUsed(response, 'crypto/content.html')
    assertContains(response, 'BTC')
    assertContains(response, 'Bitcoin')
    assertContains(response, '24h Chg')


def test_securities(client):
    response = client.get('/securities/')
    assert response.status_code == 200
    assert response.context['page'] == 'securities'
    assert response.context['assets'][0]['symbol'] is 'GME'
    assert response.context['assets'][0]['price'] > 0


def test_positions(client):
    response = client.get('/finance/positions/')
    assert response.status_code == 200
    response = client.get(reverse('positions'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'finance/positions.html')
