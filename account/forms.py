from django import forms
from django.apps import apps

User = apps.get_model(app_label="main", model_name="User")


class RegistrationForm(forms.ModelForm):
    error_css_class = "errors"
    required_css_class = "required"

    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )
