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
from django.utils.translation import gettext_lazy as _

from .forms import LoginForm, RegistrationForm


Profile = apps.get_model(app_label="main", model_name="Profile")


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

    def get(self, request, *args, **kwargs):
        profile = self.request.user.profile
        if profile is None:
            profile = Profile.objects.create_from_user(self.request.user)

        self.object = profile
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
