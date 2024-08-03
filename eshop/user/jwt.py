import datetime as dt

import jwt
from django.conf import settings
from django.http import HttpResponse

from .models import User


def get_access_token(user: User) -> str:
    """
    Generate JWT access token for the given user.

    Args:
        user (User): The user instance.

    Returns:
        str: JWT access token.
    """
    payload = {
        "id": user.id,
        "exp": dt.datetime.now(dt.UTC) + dt.timedelta(minutes=5),
        "iat": dt.datetime.now(dt.UTC),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token


def get_refresh_token(user: User) -> str:
    """
    Generate JWT refresh token for the given user.

    Args:
        user (User): The user instance.

    Returns:
        str: JWT refresh token.
    """
    payload = {
        "id": user.id,
        "exp": dt.datetime.now(dt.UTC) + dt.timedelta(days=60),
        "iat": dt.datetime.now(dt.UTC),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token


def tokens_to_response(
    response: HttpResponse,
    access_token: str = None,
    refresh_token: str = None,
) -> HttpResponse:
    """
    Set JWT access and refresh tokens in the given response.

    Args:
        response (HttpResponse): Response where cookies need to be set.

        access_token (str, optional): JWT access token.
        Defaults to None.

        refresh_token (str, optional): JWT refresh token.
        Defaults to None.

    Returns:
        HttpResponse: Response with cookies set.
    """
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


def clear_tokens(response: HttpResponse) -> HttpResponse:
    """
    Clear JWT access and refresh tokens from the given response.

    Args:
        response (HttpResponse): Response where cookies
        need to be cleared.

    Returns:
        HttpResponse: Reponse without JWT tokens.
    """
    response.delete_cookie("jwt-access")
    response.delete_cookie("jwt-refresh")
    return response
