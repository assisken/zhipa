from django import forms
from django.apps import apps
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django_registration.forms import RegistrationForm as OldRegistrationForm

CSS_CLASS = {"class": "auth-input"}
User = apps.get_model(app_label="main", model_name="User")


class ErrorCssClassMixin:
    error_css_class = "errors"
    required_css_class = "required"


class LoginForm(ErrorCssClassMixin, AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, **CSS_CLASS})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", **CSS_CLASS}
        ),
    )


class RegistrationForm(ErrorCssClassMixin, OldRegistrationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", **CSS_CLASS}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", **CSS_CLASS}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(OldRegistrationForm.Meta):
        model = User
        fields = [
            User.USERNAME_FIELD,
            "password1",
            "password2",
            User.get_email_field_name(),
            "last_name",
            "first_name",
            "middle_name",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"autofocus": True, **CSS_CLASS}),
            "email": forms.EmailInput(attrs=CSS_CLASS),
            "last_name": forms.TextInput(attrs=CSS_CLASS),
            "first_name": forms.TextInput(attrs=CSS_CLASS),
            "middle_name": forms.TextInput(attrs=CSS_CLASS),
        }
