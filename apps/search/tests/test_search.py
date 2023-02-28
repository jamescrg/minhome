import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.contacts.models import Contact
from apps.favorites.models import Favorite
from apps.folders.models import Folder
from apps.notes.models import Note

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


def test_index(user, client):
    response = client.get("/search/")
    assert response.status_code == 200

    response = client.get(reverse("search"))
    assert response.status_code == 200

    response = client.get(reverse("search"))
    assertTemplateUsed(response, "search/content.html")
    assertTemplateUsed(response, "search/form.html")


def test_results(user, client):
    favorite_folder = Folder.objects.create(user=user, name="Faves", page="favorites")
    note_folder = Folder.objects.create(user=user, name="My Notes", page="notes")
    contact_folder = Folder.objects.create(user=user, name="People", page="contacts")

    Favorite.objects.create(
        user=user,
        name="Google",
        folder=favorite_folder,
        description="Search enginge for james.",
    )

    Note.objects.create(
        user=user,
        subject="Tasks for James",
        folder=note_folder,
    )

    Contact.objects.create(
        user=user,
        name="James Craig",
        folder=contact_folder,
    )

    data = {
        "search_text": "James",
    }

    response = client.post("/search/results", data)
    assert response.status_code == 200
    assertTemplateUsed(response, "search/content.html")
    assertTemplateUsed(response, "search/results.html")

    favorites = response.context["favorites"]
    favorite = favorites.filter(name="Google").get()
    assert favorite.name == "Google"

    note = response.context["notes"]
    note = note.filter(pk=1).get()
    assert note.subject == "Tasks for James"

    contact = response.context["contacts"]
    contact = contact.filter(name="James Craig").get()
    assert contact.name == "James Craig"
