from . import settings


def env(request):
    return {
        "env": settings.ENV,
    }


def site_handle(request):
    return {
        "site_handle": settings.SITE_NAME,
    }
