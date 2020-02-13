from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import add_message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import SeveralPublicationsForm
from main.models import Publication


class SeveralPublicationsView(PermissionRequiredMixin, TemplateView):
    template_name = 'admin/publications/add_couple.html'
    permission_required = 'add_publication'
    render = {
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
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.render)

    def post(self, request, *args, **kwargs):
        form = SeveralPublicationsForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, self.render)
        data = form.cleaned_data['couple_items'].split('\n')

        for publication in data:
            publication = publication.replace(' 	', '||')
            name, place, authors = publication.split('||')
            Publication.objects.get_or_create(name=name, place=place, authors=authors)

        count = len(data)
        items = 'publications' if count > 1 else 'publication'
        add_message(request, messages.INFO, f'{count} {items} successfully added!')
        return HttpResponseRedirect('../')
