from django.urls import path

from .views import LoginFormView, LogoutView, ProfileView, RegistrationFormView

app_name = "user"

urlpatterns = [
    path("registration/", RegistrationFormView.as_view(), name="registration"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
