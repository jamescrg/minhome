import pytest
from django.test import Client

from accounts.models import CustomUser
from apps.folders.models import Folder
from apps.tasks.models import Task


@pytest.fixture
def user():
    user = CustomUser.objects.create_user("Ollie", "ollie@gmail.com", "clawboy")
    return user


@pytest.fixture
def client(user):
    client = Client()
    client.login(username="Ollie", password="clawboy")
    return client


@pytest.fixture
def folders(user):
    names = [
        "Current",
        "Chores",
        "Writing",
        "Monday",
    ]
    folders = []
    for name in names:
        folders.append(
            Folder.objects.create(
                user=user,
                page="tasks",
                name=name,
            )
        )
    return folders


@pytest.fixture
def folder(folders):
    folder = folders[0]
    folder.save()
    return folder


@pytest.fixture
def tasks(user, folder):
    descriptions = [
        "Take out trash",
        "Rake leaves",
        "Sweep back porch",
        "Scrub shower tile",
    ]
    tasks = []
    for description in descriptions:
        tasks.append(
            Task.objects.create(
                user=user,
                folder=folder,
                title=description,
                status=0,
            )
        )
    return tasks


@pytest.fixture
def task(tasks):
    task = tasks[0]
    task.save()
    return task
