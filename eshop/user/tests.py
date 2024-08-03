from django.test import RequestFactory, TestCase
from django.urls import reverse

from .forms import RegistrationForm
from .jwt import get_access_token
from .models import User
from .views import LoginFormView, LogoutView, RegistrationFormView


class AuthenticationViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            email="test1@user.com",
            first_name="test1",
            last_name="user",
            password="difficult_password_123",
        )

    def test_registration(self):
        data = {
            "email": "test2@user.com",
            "first_name": "test2",
            "last_name": "user",
            "password1": "difficult_password_123",
            "password2": "difficult_password_123",
        }

        factory = RequestFactory()

        request = factory.post(reverse("user:registration"), data=data)

        response = RegistrationFormView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="test2@user.com").exists())

    def test_profile_view(self):
        response = self.client.get(reverse("user:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url, "/accounts/login/?next=/accounts/profile/"
        )

        self.user = User.objects.get(pk=1)
        self.client.cookies["jwt-access"] = get_access_token(self.user)

        response = self.client.get(reverse("user:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Выйти из аккаунта")

    def test_login(self):
        data = {
            "email": "test1@user.com",
            "password": "difficult_password_123",
        }
        factory = RequestFactory()

        request = factory.post(reverse("user:login"), data=data)

        response = LoginFormView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.cookies.get("jwt-access", False))

    def test_logout(self):
        self.user = User.objects.get(pk=1)
        self.client.cookies["jwt-access"] = get_access_token(self.user)
        factory = RequestFactory()

        request = factory.post(reverse("user:logout"))
        request.user = self.user

        response = LogoutView.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies.get("jwt-access").value, "")
        self.assertEqual(
            response.cookies.get("jwt-refresh").value,
            "",
        )
        self.assertEqual(response.url, "/")


class UserFormTests(TestCase):
    def test_registration_form_valid(self):
        data = {
            "email": "test1@user.com",
            "first_name": "test1",
            "last_name": "user",
            "password1": "difficult_password_123",
            "password2": "difficult_password_123",
        }
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        data = {
            "email": "test1@user.com",
            "first_name": "test1",
            "last_name": "user",
            "password1": "simple",
            "password2": "simple",
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
