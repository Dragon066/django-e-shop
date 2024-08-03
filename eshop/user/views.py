import logging

from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView, View

from .forms import LoginForm, RegistrationForm
from .jwt import (
    clear_tokens,
    get_access_token,
    get_refresh_token,
    tokens_to_response,
)
from .models import User


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A profile template view.

    Displays a user's profile page using template in this class
    and request.user instance as context data.

    Login required.

    Attributes:
        template_name: The name of the template to render
        for the profile page.
    """

    template_name = "user_profile.html"


class LoginFormView(FormView):
    """
    A view for handling user login.

    This view processes a POST request containing user credentials.
    If the credentials are valid, it generates JWT tokens for the user,
    logs the user in, and redirects them to their profile page.

    Attributes:
        template_name: The name of the template to render
        for the login page.

        form_class: The form class to use for the login form.

        success_url: The URL to redirect to after a successful login.
    """

    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = "/accounts/profile/"

    def post(self, request, *args, **kwargs):
        """
        Handles a POST request for login.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseRedirect: If the user is successfully logged in,
            redirects to the profile page.

            LoginForm: If the user credentials are invalid, returns
            the login form with error messages.
        """
        form = self.get_form()
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            response = tokens_to_response(
                HttpResponseRedirect(self.get_success_url()),
                get_access_token(user),
                get_refresh_token(user),
            )

            logging.info(f'User "{user.email}" logged in successfully')

            return response
        else:
            return self.form_invalid(form)


class RegistrationFormView(FormView):
    """
    A view for handling user registration.

    This view processes a POST request containing
    user registration data.
    If the registration data is valid, it creates a new user and
    generates JWT tokens for the user,
    logs the user in, and redirects them to their profile page.

    Attributes:
        template_name: The name of the template to render
        for the login page.

        form_class: The form class to use for the login form.

        success_url: The URL to redirect to after a successful login.
    """

    template_name = "registration/registration.html"
    form_class = RegistrationForm
    success_url = "/accounts/profile/"

    def post(self, request, *args, **kwargs):
        """
        Handles a POST request for registration.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseRedirect: If the user is successfully logged in,
            redirects to the profile page with JWT tokens.

            RegistrationForm: If the user credentials are invalid,
            returns the login form with error messages.
        """
        form = self.get_form()
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if password1 != password2:
            form.add_error("password2", "Пароли не совпадают")
            return self.form_invalid(form)
        if not form.is_valid():
            return self.form_invalid(form)
        user = User.objects.create(
            email=email, first_name=first_name, last_name=last_name
        )
        user.set_password(password1)
        user.save()

        logging.info(f'User "{user.email}" registered successfully')

        if user is not None:
            response = tokens_to_response(
                HttpResponseRedirect(self.get_success_url()),
                get_access_token(user),
                get_refresh_token(user),
            )

            return response
        else:
            return self.form_invalid(form)


class LogoutView(View):
    """
    A view for handling user logout.

    This view processes a POST request for logout.
    If the user is successfully logged out, it clears the JWT tokens
    and redirects them to the root URL.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles a POST request for logout.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseRedirect: Redirects to the root URL with cleared
            JWT tokens.
        """
        response = clear_tokens(HttpResponseRedirect("/"))

        logging.info(f'User "{request.user.email}" logged out successfully')

        return response
