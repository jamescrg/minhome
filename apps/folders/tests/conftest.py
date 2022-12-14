

import pytest

from django.test import Client

from accounts.models import CustomUser
from apps.folders.models import Folder


@pytest.fixture
def user():
    user = CustomUser.objects.create_user('Ollie', 'ollie@gmail.com', 'clawboy')
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username='Ollie', password='clawboy')
    return client


@pytest.fixture
def folder(user):
    folder1 = Folder.objects.create(
        user=user,
        page='favorites',
        name='Main',
        home_column=1,
        home_rank=1,
        selected=1,
        active=1,
    )
    return folder1


@pytest.fixture
def folders(user):
    folders = [
        'Social',
        'Recipes',
        'Places',
        'Philosophy',
    ]

    for name in folders:
        Folder.objects.create(
            user=user, page='notes', name=name, home_column=0, home_rank=0
        )
    return folders

