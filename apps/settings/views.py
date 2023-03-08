import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def index(request):
    """Show the settings page.

    Notes:
        Shows whether the user has linked a Google account.
        If not, provides a url to link one.
        If so, provides a url to log out.
    """

    if request.user.google_credentials:
        logged_in = True
    else:
        logged_in = False

    context = {
        "page": "settings",
        "logged_in": logged_in,
    }
    return render(request, "settings/content.html", context)


@login_required
def google_login(request):
    """Direct the user to their login page to obtain an authorization code.

    Notes:
        Based on sample code from:
        https://developers.google.com/identity/protocols/oauth2/web-server
    """

    # sets the url to return to when an authorization code has been obtained
    redirect_uri = "https://" + request.get_host() + "/settings/google/store"

    # builds the url to go to in order to obtain the authorization code
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "/home/james/.google/cp.json",
        scopes=[
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/contacts",
        ],
    )
    flow.redirect_uri = redirect_uri

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        prompt="consent",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # this is to prevent cross site scripting attacks
    request.session["state"] = state

    return redirect(authorization_url)


@login_required
def google_store(request):
    """Store the user's authorization code in the database.

    Notes:
        The user's authorization code is a json string,
        which is stored in the user's "google_credentials" attribute.
    """

    redirect_uri = "https://" + request.get_host() + "/settings/google/store"
    pwd = settings.BASE_DIR

    state = request.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "/home/james/.google/cp.json",
        scopes=[
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/contacts",
        ],
        state=state,
    )
    flow.redirect_uri = redirect_uri

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # get the user credentials and package them as a json string
    credentials = flow.credentials
    google_credentials_json = credentials.to_json()

    # save the json credentials to the database
    user = request.user
    user.google_credentials = google_credentials_json
    user.save()

    return redirect("/settings")


@login_required
def google_logout(request):
    """Disconnects the user's google account from the app.

    Notes:
        Contacts google and revokes the user's auth code.
        Then deletes the user's code from the database.
    """

    # get / build the user credentials
    user = request.user
    credentials = user.google_credentials
    credentials = json.loads(credentials)
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
        credentials
    )

    # use the credentials to revoke access
    requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    # delete the credentials from the database
    user.google_credentials = None
    user.save()

    return redirect("/settings")


@login_required
def theme(request):
    """Sets the user's preferred  theme.

    """

    user = request.user
    user.theme = request.POST['theme']
    user.save()
    return redirect("/settings")

@login_required
def home_options(request, option, value):
    """Sets the user's home page options
    """
    user = request.user

    if not 'home' in user.settings:
        user.settings['home'] = {}

    user.settings['home'][option] = value
    user.save()
    return redirect("/settings")


@login_required
def zip(request):
    """Sets the user's zip code.

    """
    user = request.user
    user.settings['zip'] = request.POST['zip']
    user.save()
    return redirect("/settings")

@login_required
def zip_remove(request):
    """Removes the user's zip code.

    """
    user = request.user
    del user.settings['zip']
    user.save()
    return redirect("/settings")
