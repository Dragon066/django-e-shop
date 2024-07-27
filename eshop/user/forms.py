from django.contrib.auth.password_validation import validate_password
from django import forms
from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль', validators=[validate_password])
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')
    