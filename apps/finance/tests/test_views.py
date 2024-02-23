import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

pytestmark = pytest.mark.django_db


def test_crypto(client):
    response = client.get("/crypto/")
    assert response.status_code == 200
    assert response.context["page"] == "crypto"
    assert "market_cap" in response.context["data"][0]
    assertTemplateUsed(response, "finance/crypto.html")
    assertContains(response, "BTC")
    assertContains(response, "Bitcoin")
    assertContains(response, "24h Chg")


def test_securities(client):
    response = client.get("/securities/")
    assert response.status_code == 200
    assert response.context["page"] == "securities"
    assert response.context["data"][0]["price"] > 0
    assertTemplateUsed(response, "finance/securities.html")
