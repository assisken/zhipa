from django.urls import path
from django.views.generic import TemplateView

from accounts.views import (
    ActivationView,
    LoginView,
    LogoutView,
    ProfileDescriptionView,
    RegistrationView,
)

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("register/", RegistrationView.as_view(), name="registration"),
    path(
        "register/complete",
        TemplateView.as_view(template_name="accounts/registration_complete.html"),
        name="registration_complete",
    ),
    path("activate/<key:activation_key>/", ActivationView.as_view(), name="activation"),
    path(
        "complete",
        TemplateView.as_view(template_name="accounts/activation_complete.html"),
        name="activation_complete",
    ),
    path(
        "info", TemplateView.as_view(template_name="accounts/index.html"), name="index"
    ),
    path("profile", ProfileDescriptionView.as_view(), name="profile"),
]
