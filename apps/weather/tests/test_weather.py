import pytest

from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed


pytestmark = pytest.mark.django_db()


def test_index(client):
    response = client.get("/weather/")
    assert response.status_code == 200

    response = client.get(reverse("weather"))
    assert response.status_code == 200

    assertTemplateUsed(response, "weather/content.html")
    assert ":" in response.context["current"]["sunrise"]
