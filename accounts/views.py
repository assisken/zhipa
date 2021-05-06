from typing import Optional

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as OldLoginView
from django.contrib.auth.views import LogoutView as OldLogoutView
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django_registration.backends.activation.views import (
    ActivationView as OldActivationView,
)
from django_registration.backends.activation.views import (
    RegistrationView as OldRegistrationView,
)

from .forms import RegistrationForm

Profile = apps.get_model(app_label="main", model_name="Profile")
User = apps.get_model(app_label="main", model_name="User")


class LoginView(OldLoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class RegistrationView(OldRegistrationView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    email_body_template = "accounts/activation_email_body.txt"
    email_subject_template = "accounts/activation_email_subject.txt"
    success_url = reverse_lazy("accounts:registration_complete")


class ActivationView(OldActivationView):
    ALREADY_ACTIVATED_MESSAGE = _(
        "The account you tried to activate has already been activated."
    )
    BAD_USERNAME_MESSAGE = _("The account you attempted to activate is invalid.")
    EXPIRED_MESSAGE = _("This account has expired.")
    INVALID_KEY_MESSAGE = _("The activation key you provided is invalid.")

    template_name = "accounts/activation_failed.html"
    success_url = reverse_lazy("accounts:activation_complete")


class MyProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile/description.html"
    context_object_name = "profile"

    def get_object(
        self, queryset: Optional[models.query.QuerySet] = ...
    ) -> models.Model:
        return self.request.user.profile


class SettingsView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "accounts/settings.html"
    fields = ("last_name", "first_name", "middle_name")

    def get_object(
        self, queryset: Optional[models.query.QuerySet] = ...
    ) -> models.Model:
        return self.request.user
