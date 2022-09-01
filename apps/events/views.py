from datetime import date, timedelta
from dateutil import parser

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from apps.events.models import Event
from apps.events.forms import EventForm
import apps.events.google as google


@login_required
def index(request):

    today = date.today()
    third_day = today + timedelta(days=3)

    events = Event.objects.filter(status='Pending').order_by('date')

    context = {
        'page': 'events',
        'events': events,
        'third_day': third_day,
    }

    return render(request, 'events/list.html', context)


@login_required
def add(request, origin='events'):

    # identify the origin of the request (events or agenda)
    if request.method == 'GET':
        request.session['origin'] = origin
    origin = request.session.get('origin', 'events')

    # identify user
    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)

    # if applicable, process any post data submitted by user
    if request.method == 'POST':

        form = EventForm(request.POST)
        if form.is_valid():

            # initialize event data
            event = form.save(commit=False)
            event.user_id = request.user.id

            # add to google account
            if user.google_credentials:
                event.google_id = google.add_event(event)

            # save event to database with google id
            event.save()

            return redirect('events')

    # if no post data has been submitted, show the contact form
    else:
        form = EventForm()

    google_connected = user.google_credentials

    context = {
        'page': 'events',
        'edit': False,
        'add': True,
        'results': None,
        'action': '/events/add',
        'google_connected': google_connected,
        'form': form,
        'origin': origin,
    }

    return render(request, 'events/form.html', context)


@login_required
def edit(request, id, origin='events'):

    # identify the origin of the request (events or agenda)
    if request.method == 'GET':
        request.session['origin'] = origin
    origin = request.session.get('origin', 'events')

    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)

    event = get_object_or_404(Event, pk=id)

    if request.method == 'POST':

        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            event = form.save(commit=False)
            event.user_id = request.user.id

            google_connected = user.google_credentials
            if google_connected and event.google_id:
                google.edit_event(event)

            event.save()
            return redirect('events')

    else:

        form = EventForm(instance=event)


    google_connected = user.google_credentials

    context = {
        'page': 'events',
        'edit': True,
        'add': False,
        'results': None,
        'action': f'/events/{id}/edit',
        'event': event,
        'google_connected': google_connected,
        'form': form,
        'origin': origin,
    }

    return render(request, 'events/form.html', context)


@login_required
def delete(request, id, origin='events'):

    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)

    # identify the origin of the request (events or agenda)
    if request.method == 'GET':
        request.session['origin'] = origin
    origin = request.session.get('origin', 'events')

    event = get_object_or_404(Event, pk=id)

    google_connected = user.google_credentials

    if google_connected and event.google_id:
        google.delete_event(event)

    event.delete()

    return redirect('events')


@login_required
def google_sync(request, id):
    event = get_object_or_404(Event, pk=id)
    event.google_id = google.add_event(event)
    event.save()
    return redirect('/events')
