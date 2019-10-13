import re

from django.contrib import messages
from django.contrib.messages import add_message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import ExtramuralSchedule
from main.models import Schedule


class AddExtramuralSchedule(TemplateView):
    template_name = 'admin/schedule/add_extramural.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': ExtramuralSchedule(),
            'opts': Schedule._meta,
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
        form = ExtramuralSchedule(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {
                'form': form,
                'errors': form.errors,
                'opts': Schedule._meta,
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

        count = 0
        items = 'items'

        data = form.cleaned_data['schedule'].split('\n')

        for line in data:
            cleaned = list(map(lambda x: x.strip(), line.split('||')))
            dates, times, item, teachers, place = cleaned

            dates = list(map(lambda x: x.strip(), re.split(r' +', dates)))
            times = list(map(lambda x: x.strip(), re.split(r' +', times)))
            teachers = list(map(lambda x: x.strip(), re.split(r' +', teachers)))
            place = list(map(lambda x: x.strip(), re.split(r' +', place)))

        # add_message(request, messages.INFO, f'{count} {items} successfully added!')
        return HttpResponseRedirect('.')
