from django import forms
from django.contrib.admin.forms import forms as admin_forms
from django.contrib.admin import widgets as admin_widgets
from django.core.exceptions import ValidationError

from main.models import Group, Schedule


def check_items(value: str):
    items = value.split('\n')
    for line, item in enumerate(items):
        item = item.replace(' 	', '||')
        if item.count('||') != 2:
            count = item.count("||") + 1
            raise ValidationError(f'Required 3 or more items, got {count} on line {line + 1}')


class SeveralPublicationsForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    couple_items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_items,)
    )


class ExtramuralSchedule(admin_forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    group = admin_forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=admin_widgets.FilteredSelectMultiple(
            verbose_name=Group._meta.verbose_name,
            is_stacked=False
        )
    )
    schedule = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'})
    )
