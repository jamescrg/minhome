import pytest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.notes.models import Note

# This flags all tests in the file as needing database access
# Once setup, the database is cached to be used for all subsequent tests
# and rolls back transactions, to isolate tests from each other.
# This is the same way the standard Django TestCase uses the database.
# However pytest-django also caters for transaction test cases and allows you
# to keep the test databases configured across different test runs.

pytestmark = pytest.mark.django_db


def test_note_string(note):
    note = Note.objects.get(subject="Things I Like")
    assert str(note) == f"{note.subject}"


def test_note_content(note, user, folder1):
    note = Note.objects.filter(subject="Things I Like").get()
    expectedValues = {
        "user": user,
        "folder": folder1,
        "selected": 1,
        "subject": "Things I Like",
        "note": "Ice cream and cookies are nice",
    }
    for key, val in expectedValues.items():
        assert getattr(note, key) == val


def test_index(client):
    response = client.get("/notes/")
    assert response.status_code == 200
    response = client.get(reverse("notes"))
    assert response.status_code == 200
    response = client.get(reverse("notes"))
    assertTemplateUsed(response, "notes/content.html")


def test_select(client, user, folder1, note):
    response = client.get(f"/notes/{note.id}")
    assert response.status_code == 302
    selected_note = get_object_or_404(Note, pk=note.id)
    assert selected_note.selected == 1


def test_add_form(client):
    response = client.get("/notes/add")
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/form.html")


def test_add_data(client, folder1):
    data = {
        "folder": folder1.id,
        "subject": "Plato",
        "note": "A Greek philosopher",
    }
    response = client.post("/notes/add", data)
    assert response.status_code == 302
    found = Note.objects.filter(subject="Plato").exists()
    assert found


def test_edit_form(client, note):
    response = client.get(f"/notes/{note.id}/edit")
    assert response.status_code == 200
    assertTemplateUsed(response, "notes/form.html")


def test_edit_data(client, folder1, note):
    data = {
        "folder": folder1.id,
        "subject": "Descartes",
        "note": "A French philosopher",
    }
    response = client.post(f"/notes/{note.id}/edit", data)
    assert response.status_code == 302
    found = Note.objects.filter(subject="Descartes").exists()
    assert found


def test_delete(client, note):
    response = client.get(f"/notes/{note.id}/delete")
    assert response.status_code == 302
    found = Note.objects.filter(subject="Things I like").exists()
    assert not found
