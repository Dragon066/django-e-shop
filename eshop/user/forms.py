from django import forms
from django.contrib.auth.password_validation import validate_password


class LoginForm(forms.Form):
    """
    A login form for user.

    Fields:
        email (forms.EmailField): Email field.

        password (forms.CharField): Password field.
    """

    email = forms.EmailField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class RegistrationForm(forms.Form):
    """
    A registration form for user.

    Fields:
        email (forms.EmailField): Email field.

        first_name (forms.CharField): First name field.

        last_name (forms.CharField): Last name field.

        password1 (forms.CharField): First password field.

        password2 (forms.CharField): Second password field for
        confirmation.
    """

    email = forms.EmailField(label="E-mail")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        validators=[validate_password],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, label="Подтвердите пароль"
    )
