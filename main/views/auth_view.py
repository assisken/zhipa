from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_registration.backends.activation.views import (
    ActivationView,
    RegistrationView,
)

from main.forms import SmiapRegistrationForm


class SmiapLoginView(LoginView):
    template_name = "auth/login.html"
    redirect_authenticated_user = True


class SmiapLogoutView(LogoutView):
    pass


class SmiapRegistrationView(RegistrationView):
    form_class = SmiapRegistrationForm
    template_name = "auth/register.html"
    email_body_template = "auth/activation_email_body.txt"
    email_subject_template = "auth/activation_email_subject.txt"

    def post(self, request: HttpRequest, *args, **kwargs):
        form = SmiapRegistrationForm(request.POST)
        if not form.is_valid():
            return self.render_to_response(self.get_context_data())
        self.create_inactive_user(form)
        return redirect("registration_complete")


class SmiapActivationView(ActivationView):
    template_name = "auth/activation_failed.html"
    success_url = reverse_lazy("activation_complete")
