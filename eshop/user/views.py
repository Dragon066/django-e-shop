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
    template_name = "user_profile.html"


class LoginFormView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = "/accounts/profile/"

    def post(self, request, *args, **kwargs):
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
    template_name = "registration/registration.html"
    form_class = RegistrationForm
    success_url = "/accounts/profile/"

    def post(self, request, *args, **kwargs):
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
    def post(self, request, *args, **kwargs):
        response = clear_tokens(HttpResponseRedirect("/"))

        logging.info(f'User "{request.user.email}" logged out successfully')

        return response
