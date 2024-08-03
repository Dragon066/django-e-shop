import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from .jwt import get_access_token, tokens_to_response

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Custom JWT Authentication middleware for Django.
    """

    def process_request(self, request):
        """
        Process request to authenticate user using JWT token.

        If token is valid, it sets the user in the request. Otherwise,
        it sets the AnonymousUser object in the request.

        If access token has expired, it updates with the refresh token.

        Args:
            request: The HTTP request object.

        Returns:
            User: The authenticated user.

            AnonymousUser: The AnonymousUser object.
        """
        token = request.COOKIES.get("jwt-access")
        if token:
            try:
                payload = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )
                request.user = User.objects.get(id=payload["id"])
            except jwt.ExpiredSignatureError:
                refresh = request.COOKIES.get("jwt-refresh")
                try:
                    payload = jwt.decode(
                        refresh, settings.SECRET_KEY, algorithms=["HS256"]
                    )
                    user = User.objects.get(id=payload["id"])
                    request.user = user
                    response = tokens_to_response(
                        self.get_response(request),
                        access_token=get_access_token(user),
                    )
                    return response
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    request.user = AnonymousUser()
            except (jwt.InvalidTokenError, User.DoesNotExist):
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
