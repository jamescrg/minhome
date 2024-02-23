import pytest
from django.test.client import RequestFactory

from apps.home.toggle import show_section

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


def test_default_state(client):
    """Verify that sections are shown when selected by the user"""

    response = client.get("/")
    context = response.context
    assert response.status_code == 200
    assert context["show_events"]
    assert context["show_tasks"]


def test_toggle_redirect(client):
    # toggle view redirects to index
    response = client.get("/home/toggle/events")
    assert response.status_code == 302


def test_toggle_section(client):

    # client initial values are client.home_events == 1 and
    # show_events_hidden == 1980-01-01, an expired date,
    # therefore, ""show_events"" would evaluate to True
    response = client.get("/")
    context = response.context
    assert context["show_events"]

    # toggle the events section
    response = client.get("/home/toggle/events")
    assert response.status_code == 302

    # now that events have been toggled, they should be switched off
    response = client.get("/")
    context = response.context
    assert not context["show_events"]
