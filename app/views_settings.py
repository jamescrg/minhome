from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

import google.oauth2.credentials
import google_auth_oauthlib.flow
import json

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

    # credentials from google
    # client_id = settings.GOOGLE_CLIENT_ID
    # client_secret = settings.GOOGLE_CLIENT_SECRET
    redirect_uri = 'https://lab.cloud-portal.com/settings/google/store'
    pwd = settings.BASE_DIR

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        f'{pwd}/cp_credentials_web.json',
        scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/contacts'])
    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    request.session['state'] = state

    return redirect(authorization_url)


@login_required
def google_store(request):

    redirect_uri = 'https://lab.cloud-portal.com/settings/google/store'
    pwd = settings.BASE_DIR

    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        f'{pwd}/cp_credentials_web.json',
        scopes=['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/contacts'], 
        state=state)
    flow.redirect_uri = redirect_uri

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # get the user credentials and package them as a json string
    credentials = flow.credentials
    google_credentials = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
        }
    google_credentials_json = json.dumps(google_credentials)

    # save the json credentials to the database
    user_id = request.user.id
    user = get_object_or_404(CustomUser, pk=user_id)
    user.google_credentials = google_credentials_json
    user.save()

    return redirect('/settings')


