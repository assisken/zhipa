from django import forms
from django.contrib import messages
from django.contrib.messages import add_message
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Publication


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
            raise ValidationError(f'{" 	" in item and item.count(" 	") != 2} Required 3 or more items, got {count} on line {line + 1}')


class SeveralPublicationsForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    couple_items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_items,)
    )


class SeveralPublicationsView(TemplateView):
    template_name = 'admin/publications/add_couple.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': SeveralPublicationsForm(),
            'opts': Publication._meta,
            'change': False,
            'is_popup': False,
            'save_as': True,
            'has_delete_permission': False,
            'has_add_permission': True,
            'has_change_permission': False,
            'add': True,
            'has_view_permission': True,
            'has_editable_inline_admin_formsets': True,
        })

    def post(self, request, *args, **kwargs):
        form = SeveralPublicationsForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'errors': form.errors,
                'opts': Publication._meta,
                'change': False,
                'is_popup': False,
                'save_as': True,
                'has_delete_permission': False,
                'has_add_permission': True,
                'has_change_permission': False,
                'add': True,
                'has_view_permission': True,
                'has_editable_inline_admin_formsets': True,
            })
        for publication in form.cleaned_data['couple_items'].split('\n'):
            if ' 	' in publication:
                name, place, authors = publication.split(' 	')
            else:
                name, place, authors = publication.split('||')
            Publication.objects.get_or_create(name=name, place=place, authors=authors)

        add_message(request, messages.INFO, 'Items successfully added!')
        return HttpResponseRedirect('../')
