import re

from django import forms
from django.core.exceptions import ValidationError

from main.models import User


def check_items(value: str):
    items = value.split('\n')
    for line, item in enumerate(items):
        item = item.replace(' 	', '||')
        if item.count('||') != 2:
            count = item.count("||") + 1
            raise ValidationError(f'Required 3 or more items, got {count} on line {line + 1}')


class GeneralForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'


class SmiapRegistrationForm(GeneralForm):
    class Meta:
        model = User
        fields = ("email", "username",)


class SeveralPublicationsForm(GeneralForm):
    couple_items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_items,)
    )


