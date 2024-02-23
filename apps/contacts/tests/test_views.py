import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from apps.contacts.models import Contact
from accounts.models import CustomUser

pytestmark = pytest.mark.django_db


def test_index(client, folder1, contact):
    response = client.get("/contacts/")
    assert response.status_code == 200

    response = client.get(reverse("contacts"))
    assert response.status_code == 200

    # no selected folder
    response = client.get(reverse("contacts"))
    assertTemplateUsed(response, "contacts/content.html")
    assert not response.context["contacts"]

    # folder selected
    response = client.get(f"/folders/{folder1.id}/contacts")
    response = client.get(reverse("contacts"))
    assert response.context["contacts"]


def test_select(client, user, folder1, contact):
    response = client.get(f"/contacts/{contact.id}")
    assert response.status_code == 302
    user = get_object_or_404(CustomUser, pk=user.id)
    assert user.contacts_contact == contact.id


def test_add_get(client, folder1):
    # test without a selected folder
    response = client.get("/contacts/add")
    assert response.status_code == 200
    assertTemplateUsed(response, "contacts/form.html")

    # set a selected folder
    response = client.get(f"/folders/{folder1.id}/contacts")
    response = client.get("/contacts/add")
    assert folder1 in response.context["folders"]
    assert response.status_code == 200


def test_add_post(client, contact):
    # set a selected contact
    contact.selected = 1
    contact.save()

    # set data to use
    data = {
        "folder_id": 88,
        "selected": 0,
        "name": "Stacey McReynolds",
        "company": "",
        "address": "170 Ivy Glen Circle\r\nAvondale Estates, GA 30002",
        "phone1": "404.273.4347",
        "phone1_label": "Work",
        "phone2": "404.477.4217",
        "phone2_label": "Work",
        "phone3": "",
        "phone3_label": "Work",
        "email": "donothave@gmail.com",
        "website": "",
        "map": "",
        "notes": "",
        "google_id": "people/c4669684526832277027",
    }

    response = client.post("/contacts/add", data)
    assert response.status_code == 302

    found = Contact.objects.filter(name="Stacey McReynolds").get()
    assert found
    assert found.selected == 1


def test_edit_get(client, contact):
    response = client.get(f"/contacts/{contact.id}/edit")
    assert response.status_code == 200
    assertTemplateUsed(response, "contacts/form.html")


def test_edit_post(client, folder1, contact):
    # test normal
    data = {
        "folder": folder1.id,
        "name": "Descartes",
        "phone1": "440.500.6000",
    }
    response = client.post(f"/contacts/{contact.id}/edit", data)
    assert response.status_code == 302
    found = Contact.objects.filter(name="Descartes").exists()
    assert found

    # test where contact not found
    # response = client.post(f'/contacts/1000/edit', data)
    # assert pytest.raises(ObjectDoesNotExist)


def test_delete(client, contact):
    response = client.get(f"/contacts/{contact.id}/delete")
    assert response.status_code == 302
    found = Contact.objects.filter(name="Schopenhauer").exists()
    assert not found
