from django.contrib.auth.views import LoginView as OldLoginView
from django.contrib.auth.views import LogoutView as OldLogoutView
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_registration.backends.activation.views import (
    ActivationView as OldActivationView,
)
from django_registration.backends.activation.views import (
    RegistrationView as OldRegistrationView,
)

from .forms import RegistrationForm


class LoginView(OldLoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True


class LogoutView(OldLogoutView):
    pass


class RegistrationView(OldRegistrationView):
    form_class = RegistrationForm
    template_name = "account/register.html"
    email_body_template = "account/activation_email_body.txt"
    email_subject_template = "account/activation_email_subject.txt"

    def post(self, request: HttpRequest, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data())
        self.create_inactive_user(form)
        return redirect("registration_complete")


class ActivationView(OldActivationView):
    template_name = "account/activation_failed.html"
    success_url = reverse_lazy("activation_complete")
