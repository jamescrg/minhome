

def index()
    page = 'settings'
    user_id = request.user.id
    user = User::findOrFail(user_id)
    return view('settings/content', context)


def googleLogin()
    page = 'settings'
    gmail = Auth::user().email
    client = GoogleClientHandler::newClient(gmail)
    GoogleClientHandler::getAuthCode(client)


def googleStore()
    code = Request::input('code')
    client = GoogleClientHandler::newClient(Auth::user().email)
    accessToken = GoogleClientHandler::getNewAccessToken(client, code)
    user_id = request.user.id
    user = User::findOrFail(user_id)
    user.google_token = accessToken
    user.save()
    return redirect('/settings/')


def googleLogout()
    user_id = request.user.id
    user = User::findOrFail(user_id)
    user.google_token = null
    user.save()
    return redirect('/settings/')
    


