import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.tasks.models import Task

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


# ------------------------------------
# urls and templates
# ------------------------------------


def test_content(client, user, tasks, folders):
    task = tasks[0]
    expectedValues = {
        "user": user,
        "folder": folders[0],
        "title": "Take out trash",
        "status": 0,
    }
    for key, val in expectedValues.items():
        assert getattr(task, key) == val


def test_string(client, tasks):
    task = tasks[0]
    expected = "{} : {}".format(task.title, task.id)
    assert str(task) == expected


# ------------------------------------
# task functionality
# ------------------------------------


def test_index(client):
    response = client.get("/tasks/")
    assert response.status_code == 200

    response = client.get(reverse("tasks"))
    assert response.status_code == 200

    response = client.get(reverse("tasks"))
    assertTemplateUsed(response, "tasks/content.html")


def test_status(client, task):
    response = client.get(f"/tasks/{task.id}/complete")
    assert response.status_code == 302
    task = Task.objects.filter(pk=task.id).get()
    assert task.status == 1


def test_add_data(user, client, folder):
    data = {
        "user": user,
        "folder_id": folder.id,
        "title": "Sweep garage",
    }
    response = client.post("/tasks/add", data)
    assert response.status_code == 302
    found = Task.objects.filter(folder=folder).exists()
    assert found


def test_edit(client, task):
    response = client.get(f"/tasks/{task.id}/edit")
    assert response.status_code == 200
    assert response.context["page"] == "tasks"
    assertTemplateUsed(response, "tasks/form.html")


def test_edit_data(user, client, folder, task):
    data = {
        "user": user,
        "folder_id": folder.id,
        "title": "Sweep garage",
    }
    response = client.post(f"/tasks/{task.id}/edit", data)
    assert response.status_code == 302
    found = Task.objects.filter(title="Sweep garage").exists()
    assert found


def test_clear(client, folder):
    tasks = Task.objects.filter(folder=folder).update(status=1)
    client.get("/tasks/clear")
    tasks = Task.objects.filter(folder=folder)
    assert not tasks
