
from pprint import pprint
import json
import requests

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

import google.oauth2.credentials
import google_auth_oauthlib.flow
from apiclient.discovery import build

from accounts.models import CustomUser

@login_required
def index(request):
    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)

    if user.google_credentials:
        logged_in = True
    else:
        logged_in = False

    context = {
        'page': 'settings',
        'logged_in': logged_in,
    }
    return render(request, 'settings/content.html', context)

@login_required
def google_login(request):
    # direct the user to their login page to obtain an authorization code
    # based on sample code from https://developers.google.com/identity/protocols/oauth2/web-server
    
    # sets the url to return to when an authorization code has been obtained
    redirect_uri = 'https://lab.cloud-portal.com/settings/google/store'

    # builds the url to go to in order to obtain the authorization code
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        '/home/james/.google/cp.json',
        scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/contacts'])
    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        prompt='consent',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # this is to prevent cross site scripting attacks
    request.session['state'] = state

    return redirect(authorization_url)

@login_required
def google_store(request):
    redirect_uri = 'https://lab.cloud-portal.com/settings/google/store'
    pwd = settings.BASE_DIR

    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        '/home/james/.google/cp.json',
        scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/contacts'], 
        state=state)
    flow.redirect_uri = redirect_uri

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # get the user credentials and package them as a json string
    credentials = flow.credentials
    google_credentials_json = credentials.to_json()

    # save the json credentials to the database
    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)
    user.google_credentials = google_credentials_json
    user.save()

    return redirect('/settings')

@login_required
def show(request):
    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)
    credentials = user.google_credentials
    credentials = json.loads(credentials)
    import app.util as util
    return util.dump(credentials)


@login_required
def google_logout(request):
    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)
    credentials = user.google_credentials

    credentials = json.loads(credentials)
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(credentials)

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

    user.google_credentials = None
    user.save()

    return redirect('/settings')
