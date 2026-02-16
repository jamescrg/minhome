import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.notes.models import Note

pytestmark = pytest.mark.django_db


def test_note_string(note):
    note = Note.objects.get(title="Things I Like")
    assert str(note) == f"{note.title}"


def test_note_content(note, user, folder1):
    note = Note.objects.filter(title="Things I Like").get()
    expectedValues = {
        "user": user,
        "folder": folder1,
        "title": "Things I Like",
        "content": "Ice cream and cookies are nice",
    }
    for key, val in expectedValues.items():
        assert getattr(note, key) == val


def test_index(client):
    response = client.get("/notes/")
    assert response.status_code == 200
    response = client.get(reverse("notes:index"))
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/main.html")


def test_list(client):
    response = client.get(reverse("notes:list"))
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/list.html")


def test_add_form(client):
    response = client.get(reverse("notes:add"))
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/form.html")


def test_add_data(client, folder1):
    data = {
        "folder": folder1.id,
        "title": "Plato",
    }
    response = client.post(reverse("notes:add"), data)
    assert response.status_code == 200  # Returns HTML with script tag
    found = Note.objects.filter(title="Plato").exists()
    assert found


def test_edit_form(client, note):
    response = client.get(reverse("notes:edit", args=[note.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/form.html")


def test_edit_data(client, folder1, note):
    data = {
        "folder": folder1.id,
        "title": "Descartes",
    }
    response = client.post(reverse("notes:edit", args=[note.id]), data)
    assert response.status_code == 204
    found = Note.objects.filter(title="Descartes").exists()
    assert found


def test_delete(client, note):
    response = client.post(reverse("notes:delete", args=[note.id]))
    assert response.status_code == 204
    found = Note.objects.filter(title="Things I Like").exists()
    assert not found


def test_editor_view(client, note):
    response = client.get(reverse("notes:note-view", args=[note.id]))
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/editor.html")


def test_autosave(client, note):
    response = client.post(
        reverse("notes:note-autosave", args=[note.id]),
        {"content": "Updated content"},
    )
    assert response.status_code == 200
    note.refresh_from_db()
    assert note.content == "Updated content"


def test_title_update(client, note):
    response = client.post(
        reverse("notes:note-title", args=[note.id]),
        {"title": "New Title"},
    )
    assert response.status_code == 200
    note.refresh_from_db()
    assert note.title == "New Title"
