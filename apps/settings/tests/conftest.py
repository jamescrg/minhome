import pytest

from django.test import Client

from accounts.models import CustomUser
from apps.notes.models import Note
from apps.folders.models import Folder


@pytest.fixture
def user():
    user = CustomUser.objects.create_user("Ollie", "ollie@gmail.com", "clawboy")
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username="Ollie", password="clawboy")
    return client
