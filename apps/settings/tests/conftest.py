import pytest
from django.test import Client

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.notes.models import Note


@pytest.fixture
def user():
    user = CustomUser.objects.create_user("Ollie", "ollie@gmail.com", "clawboy")
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username="Ollie", password="clawboy")
    return client
