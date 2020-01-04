import logging
import re
import traceback

from django.contrib import messages
from django.contrib.messages import add_message
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import ExtramuralScheduleForm
from main.models import FullTimeSchedule, ExtramuralSchedule, Day, Teacher, Place


class AddExtramuralSchedule(TemplateView):
    template_name = 'admin/extramural_schedule/add_extramural.html'
    render = {
        'form': ExtramuralScheduleForm(),
        'opts': ExtramuralSchedule._meta,
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
        form = ExtramuralScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update({
                'form': form,
                'errors': form.errors,
                'opts': ExtramuralSchedule._meta,
            })
            return render(request, self.template_name, self.render)

        count = 0
        items = 'items'

        groups: QuerySet = form.cleaned_data['group']
        schedule_type = form.cleaned_data['schedule_type']
        data = form.cleaned_data['schedule'].split('\n')

        for line in data:
            cleaned = list(map(lambda x: x.strip(), line.split('||')))
            try:
                days_data, starts_at_data, item, teachers_data, places_data = cleaned
            except ValueError:
                add_message(request, messages.ERROR, f'Error with values at line:\n{cleaned}')
                return render(request, self.template_name, self.render.update({
                    'form': form,
                    'errors': form.errors,
                    'opts': FullTimeSchedule._meta,
                }))

            # date || beg_time || item || teacher || place[0] place[1]
            # 14.01.2020||16:30||Технологии удаленного обучения||Хорошко Л.Л.||413В м. Молодежная
            days_data = tuple(map(lambda x: x.strip(), re.split(r'\s+', days_data)))
            starts_at_data = tuple(map(lambda x: x.strip(), re.split(r'\s+', starts_at_data)))
            teachers_data = tuple(map(lambda x: x.strip(), re.split(r'/', teachers_data)))
            places_data = places_data.split(' ', maxsplit=1)

            try:
                days = tuple(Day.objects.get_or_create(day=day.split('.')[0],
                                                       month=day.split('.')[1],
                                                       week_day='')[0]
                             if day.lower() not in ('none', 'null', 'nil') else None
                             for day in days_data)
                starts_at = tuple(start
                                  if start.lower() not in ('none', 'null', 'nil') else None
                                  for start in starts_at_data)
                teachers = tuple(Teacher.objects.get_or_create(lastname=teacher.split(' ')[0],
                                                               firstname=teacher.split(' ')[1][0],
                                                               middlename=teacher.split(' ')[1][2])[0]
                                 if teacher.lower() not in ('none', 'null', 'nil') else None
                                 for teacher in teachers_data)
                place = Place.objects.get_or_create(building=places_data[1],
                                                    number=places_data[0])[0]

                for index, day in enumerate(days):
                    _starts_at = starts_at[index]
                    if _starts_at is None and day is None:
                        schedule = ExtramuralSchedule.objects.create(
                            starts_at=starts_at[index],
                            ends_at=None,
                            day=day,
                            item_type=ExtramuralSchedule.EMPTY,
                            schedule_type=schedule_type,
                            name=item,
                        )
                    else:
                        schedule, _ = ExtramuralSchedule.objects.get_or_create(
                            starts_at=starts_at[index],
                            ends_at=None,
                            day=day,
                            item_type=ExtramuralSchedule.EMPTY,
                            schedule_type=schedule_type,
                            name=item,
                        )
                    schedule.places.set((place,))
                    schedule.groups.add(*groups)
                    if teachers != (None,):
                        schedule.teachers.set(teachers)
            except Exception as e:
                trace = traceback.format_exc()
                logging.error(e)
                form.add_error('schedule', f'line: "{"||".join(cleaned)}"    {trace}')
                self.render.update({
                    'form': form,
                    'errors': form.errors,
                    'opts': ExtramuralSchedule._meta,
                })
                return render(request, self.template_name, self.render)
            count += 1

        add_message(request, messages.INFO, f'{count} {items} successfully added!')
        return HttpResponseRedirect('../')
