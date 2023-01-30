

import pytest

from django.test import Client

from accounts.models import CustomUser
from apps.notes.models import Note
from apps.folders.models import Folder


@pytest.fixture
def user():
    user = CustomUser.objects.create_user('Ollie', 'ollie@gmail.com', 'clawboy')
    return user


@pytest.fixture
def folder1(user):
    folder1 = Folder.objects.create(user=user, page='notes', name='Mahatmas',)
    return folder1


@pytest.fixture
def client(user):
    client = Client()
    client.login(username='Ollie', password='clawboy')
    return client


@pytest.fixture
def note(user, folder1):
    note = Note.objects.create(
        user=user,
        folder=folder1,
        selected=1,
        subject='Things I Like',
        note='Ice cream and cookies are nice',)
    note.save()
    return note
