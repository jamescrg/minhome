from . import settings


def env(request):
    return {
        "env": settings.ENV,
    }


def site_handle(request):
    return {
        "site_handle": settings.SITE_NAME,
    }


def theme(request):
    if hasattr(request, "session") and "theme" in request.session:
        return {"theme": request.session["theme"]}
    if hasattr(request, "user") and request.user.is_authenticated:
        return {"theme": request.user.theme}
    return {"theme": ""}
