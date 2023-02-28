import pytest
from django.test import Client

from accounts.models import CustomUser
from apps.favorites.models import Favorite
from apps.folders.models import Folder


@pytest.fixture
def user():
    user = CustomUser.objects.create_user("Ollie", "ollie@gmail.com", "clawboy")
    return user


@pytest.fixture
def folder1(user):
    folder1 = Folder.objects.create(
        user=user,
        page="favorites",
        name="Meditation",
    )
    return folder1


@pytest.fixture
def client(user):
    client = Client()
    client.login(username="Ollie", password="clawboy")
    return client


@pytest.fixture
def favorite(user, folder1):
    contact = Favorite.objects.create(
        user=user,
        folder=folder1,
        name="Meditation Posture",
        url="http://meditationposture.net",
        description="A website",
        login="drachma",
        root="rupee",
        passkey="ruble",
        selected=1,
    )
    return contact
