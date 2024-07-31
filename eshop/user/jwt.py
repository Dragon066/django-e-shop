import datetime as dt
import jwt
from django.conf import settings


def get_access_token(user):
    payload = {
        "id": user.id,
        "exp": dt.datetime.now(dt.UTC) + dt.timedelta(minutes=5),
        "iat": dt.datetime.now(dt.UTC),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token


def get_refresh_token(user):
    payload = {
        "id": user.id,
        "exp": dt.datetime.now(dt.UTC) + dt.timedelta(days=60),
        "iat": dt.datetime.now(dt.UTC),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token


def tokens_to_response(response, access_token=None, refresh_token=None):
    response.data = {}

    if access_token:
        response.set_cookie(
            key="jwt-access", value=access_token, httponly=True
        )
        response.data["jwt-access"] = access_token

    if refresh_token:
        response.set_cookie(
            key="jwt-refresh", value=refresh_token, httponly=True
        )
        response.data["jwt-refresh"] = refresh_token

    return response


def clear_tokens(response):
    response.delete_cookie("jwt-access")
    response.delete_cookie("jwt-refresh")
    return response
