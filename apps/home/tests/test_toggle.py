
import pytest

from django.test.client import RequestFactory

from apps.home.toggle import show_section
from apps.home.toggle import change_session

pytestmark = pytest.mark.django_db(transaction=True, reset_sequences=True)


def test_default_state(client):
    """Verify that sections are shown by default"""

    response = client.get('/')
    context = response.context
    assert response.status_code == 200
    assert context['show_events']
    assert context['show_tasks']


def test_toggle(client):
    """Check to see that sections toggle shown/hidden correctly"""

    # disallowed section
    response = client.get('/home/toggle/1')
    assert response.status_code == 302
    assert not client.session.get('events_hide_expire', False)

    # events
    response = client.get('/home/toggle/events')
    assert response.status_code == 302
    response = client.get('/')
    context = response.context
    assert response.status_code == 200
    assert not context['show_events']
    assert not client.session['show_events']
    assert client.session['events_hide_expire']

    # tasks
    response = client.get('/home/toggle/tasks')
    assert response.status_code == 302
    response = client.get('/')
    context = response.context
    assert response.status_code == 200
    assert not context['show_tasks']
    assert not client.session['show_tasks']
    assert client.session['tasks_hide_expire']

    # gathas
    response = client.get('/home/toggle/gathas')
    assert response.status_code == 302
    response = client.get('/')
    context = response.context
    assert response.status_code == 200
    assert not client.session['show_gathas']
    assert client.session['gathas_hide_expire']


def test_change_session(client):
    """ test a function that changes session data"""
    client.get('/home')
    session = client.session
    change_session(session)
    assert session['motto'] == 'Stuff happens.'
