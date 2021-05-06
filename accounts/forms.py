from django.apps import apps
from django_registration.forms import RegistrationForm as OldRegistrationForm

User = apps.get_model(app_label="main", model_name="User")


class ErrorCssClassMixin:
    error_css_class = "errors"
    required_css_class = "required"


class RegistrationForm(ErrorCssClassMixin, OldRegistrationForm):
    class Meta(OldRegistrationForm.Meta):
        model = User
        fields = [
            User.get_email_field_name(),
            User.USERNAME_FIELD,
            "password1",
            "password2",
        ]
