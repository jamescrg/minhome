
import pytest
import json
import apps.finance.tests.sample_crypto_data as sample_data

from django.test import Client
from accounts.models import CustomUser


@pytest.fixture
def sample_crypto_data():
    data = sample_data.sample_data
    return json.loads(data)


@pytest.fixture
def user():
    user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username='john', password='johnpassword')
    return client
