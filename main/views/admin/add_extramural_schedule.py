import re

from django.contrib import messages
from django.contrib.messages import add_message
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import ExtramuralScheduleForm
from main.models import Schedule, ExtramuralSchedule


class AddExtramuralSchedule(TemplateView):
    template_name = 'admin/schedule/add_extramural.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': ExtramuralScheduleForm(),
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
        form = ExtramuralScheduleForm(request.POST)
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

        groups: QuerySet = form.cleaned_data['group']
        data = form.cleaned_data['schedule'].split('\n')

        for line in data:
            cleaned = list(map(lambda x: x.strip(), line.split('||')))
            try:
                days, times, item, teachers, places = cleaned
            except ValueError:
                add_message(request, messages.ERROR, f'Error with values at line:\n{cleaned}')
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

            days = list(map(lambda x: x.strip(), re.split(r'\s+', days)))
            times = list(map(lambda x: x.strip(), re.split(r'\s+', times)))
            teachers = list(map(lambda x: x.strip(), re.split(r'\s{2,}', teachers)))
            places = list(map(lambda x: x.strip(), places.split('м.')))
            print(line)
            print(cleaned)
            print(days)
            print(times)
            print(teachers)
            print(places)

            schedule, _ = ExtramuralSchedule.objects.get_or_create(
                days='<br>'.join(days),
                times='<br>'.join(times),
                item=item,
                teachers=', '.join(teachers),
                places='<br>м.&nbsp'.join(places)
            )
            schedule.groups.set(groups)
            count += 1

        add_message(request, messages.INFO, f'{count} {items} successfully added!')
        return HttpResponseRedirect('../')
