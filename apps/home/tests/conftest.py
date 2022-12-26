

import pytest

from django.test import Client

from accounts.models import CustomUser
from apps.favorites.models import Favorite
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
def folders(user):

    folder_data = [
        # column 1
        {
            'name': 'Main',
            'home_column': 1,
            'home_rank': 1,
        },
        {
            'name': 'Entertainment',
            'home_column': 1,
            'home_rank': 2,
        },
        {
            'name': 'Local',
            'home_column': 1,
            'home_rank': 3,
        },
        {
            'name': 'Social',
            'home_column': 1,
            'home_rank': 4,
        },
        # column 2
        {
            'name': 'Dev',
            'home_column': 2,
            'home_rank': 1,
        },
        {
            'name': 'Research',
            'home_column': 2,
            'home_rank': 2,
        },
        {
            'name': 'Filing',
            'home_column': 2,
            'home_rank': 3,
        },
        {
            'name': 'Food',
            'home_column': 2,
            'home_rank': 4,
        },
        # column 3
        {
            'name': 'Philosophy',
            'home_column': 3,
            'home_rank': 1,
        },
        {
            'name': 'Psych',
            'home_column': 3,
            'home_rank': 2,
        },
        {
            'name': 'History',
            'home_column': 3,
            'home_rank': 3,
        },
        {
            'name': 'Math',
            'home_column': 3,
            'home_rank': 4,
        },
        # column 4
        {
            'name': 'Physics',
            'home_column': 4,
            'home_rank': 1,
        },
        {
            'name': 'Anthro',
            'home_column': 4,
            'home_rank': 2,
        },
        {
            'name': 'Chorus',
            'home_column': 4,
            'home_rank': 3,
        },
        {
            'name': 'Annoying',
            'home_column': 4,
            'home_rank': 4,
        },
    ]

    folders = []
    for folder in folder_data:
        folders.append(
            Folder.objects.create(
                user=user,
                name=folder['name'],
                home_column=folder['home_column'],
                home_rank=folder['home_rank'],
                page='favorites',
            )
        )

    return folders


@pytest.fixture
def favorites(user, folders):

    favorites = []
    for i in range(1, 6):
        favorites.append(
            Favorite.objects.create(
                user=user,
                folder_id=1,
                name=f'Favorite No. {i}',
                description=f'Awesome {i}',
                home_rank=i,
            )
        )

    return favorites
