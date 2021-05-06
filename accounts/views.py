from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as OldLoginView
from django.contrib.auth.views import LogoutView as OldLogoutView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django_registration.backends.activation.views import (
    ActivationView as OldActivationView,
)
from django_registration.backends.activation.views import (
    RegistrationView as OldRegistrationView,
)

from .forms import LoginForm, RegistrationForm

Staff = apps.get_model(app_label="main", model_name="Staff")


class LoginView(OldLoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class LogoutView(OldLogoutView):
    pass


class RegistrationView(OldRegistrationView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    email_body_template = "accounts/activation_email_body.txt"
    email_subject_template = "accounts/activation_email_subject.txt"
    success_url = reverse_lazy("accounts:registration_complete")

    # TODO: send mail to user


class ActivationView(LoginRequiredMixin, OldActivationView):
    template_name = "accounts/activation_failed.html"
    success_url = reverse_lazy("activation_complete")


class ProfileDescriptionView(LoginRequiredMixin, DetailView):
    model = Staff
    template_name = "profile/description.html"
    context_object_name = "profile"
