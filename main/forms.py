from django import forms
from django.core.exceptions import ValidationError


def check_items(value: str):
    items = value.split('\n')
    for line, item in enumerate(items):
        if ' 	' or item:
            if item.count(' 	') != 2:
                count = item.count(' 	') + 1
                raise ValidationError(f'(dad) Required 3 or more items, got {count} on line {line + 1}')
            return
        elif item.count('||') != 2:
            count = item.count("||") + 1
            raise ValidationError(
                f'{" 	" in item and item.count(" 	") != 2} Required 3 or more items, got {count} on line {line + 1}')


class SeveralPublicationsForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    couple_items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_items,)
    )
