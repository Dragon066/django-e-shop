from django.urls import path, include
from .views import ProfileView, LoginFormView, RegistrationFormView, LogoutView

app_name = "user"

urlpatterns = [
    path("registration/", RegistrationFormView.as_view(), name="registration"),
    path("login/", LoginFormView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
