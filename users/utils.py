from datetime import timedelta
from django.conf import settings

REFRESH_COOKIE_NAME = "refresh_token"

COOKIE_SECURE = False  # set True in production
COOKIE_SAMESITE = "Lax"
COOKIE_DOMAIN = None


def set_refresh_cookie(response, refresh_token: str):
    refresh_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        domain=COOKIE_DOMAIN,
        max_age=int(refresh_lifetime.total_seconds()),
        path="/api/",
    )


def clear_refresh_cookie(response):
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/api/",
        domain=COOKIE_DOMAIN,
    )
