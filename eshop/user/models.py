from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user manager with email as the unique identifier.
    """

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Не указан E-mail")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with given email and password.

        Args:
            email (str): E-mail address.

            password (str, optional): Password. Defaults to None.

        Returns:
            User: a new User instance with given email and password.
        """
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with given email and password.

        Args:
            email (str): E-mail address.

            password (str, optional): Password. Defaults to None.

        Returns:
            User: a new User instance with given email and password
            and superuser privileges.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    E-mail is an unique identificator.
    """

    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(
        max_length=255, blank=True, verbose_name="Фамилия"
    )
    email = models.EmailField(
        unique=True, max_length=255, verbose_name="E-mail"
    )

    is_active = models.BooleanField(default=True, verbose_name="Активный")
    is_staff = models.BooleanField(default=False, verbose_name="Администрация")
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
