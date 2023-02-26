import pytest

from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed


pytestmark = pytest.mark.django_db


def test_url(client):
    response = client.get("/settings/")
    assert response.status_code == 200


def test_named_route(client):
    response = client.get(reverse("settings"))
    assert response.status_code == 200


def test_correct_template(client):
    response = client.get(reverse("settings"))
    assertTemplateUsed(response, "settings/content.html")
