import os
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib.flatpages.forms import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage
from django.core.exceptions import ValidationError
from djangoeditorwidgets.widgets import MonacoEditorWidget

from main.models import User


def check_items(value: str):
    items = value.split("\n")
    for line, item in enumerate(items):
        item = item.replace(" 	", "||")
        if item.count("||") != 2:
            count = item.count("||") + 1
            raise ValidationError(
                f"Required 3 or more items, got {count} on line {line + 1}"
            )


class GeneralForm(forms.Form):
    error_css_class = "errors"
    required_css_class = "required"


class SmiapRegistrationForm(GeneralForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
        )


class SeveralPublicationsForm(GeneralForm):
    couple_items = forms.CharField(
        widget=forms.Textarea(attrs={"class": "vLargeTextField"}),
        validators=(check_items,),
    )


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=MonacoEditorWidget(attrs={"data-minimap": "true"}))
    template_name = forms.ChoiceField(
        help_text="Используйте default.html, если не уверены.",
        initial="flatpages/default.html",
        choices=(
            (f"flatpages/{path.name}", path.name)
            for path in Path(os.path.join(settings.TEMPLATE_DIR, "flatpages")).rglob(
                "*.html"
            )
        ),
    )

    class Meta:
        model = FlatPage
        fields = "__all__"
