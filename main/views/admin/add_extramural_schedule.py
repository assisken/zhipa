import re
from typing import Tuple, List, Optional

from django.contrib import messages
from django.contrib.messages import add_message
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import ExtramuralScheduleForm, DATE_FORMAT, PLACE_FORMAT
from main.models import ExtramuralSchedule, Day, Place, Teacher
from smiap.settings import log


class AddExtramuralSchedule(TemplateView):
    """На данной странице возможно добавление сразу нескольких элементов расписания как для сессии, так и для учебного
    времени.

    Group: Выберите, к каким группам привяжется расписание (можно выбрать несколько через Ctrl)
    Schedule type: В каком расписании отобразится вставляемые данные
    Separator: Разделитель столбцов из поля Schedule. Пока неактивен.
    Schedule: Поле, в которые вставляются само расписание по шаблону.

    На данный момент принят следующий шаблон:
    DD.MM || HH:MM || Предмет || Преподаватель И.О. || Кабинет Площадка
    DD.MM || HH:MM || Предмет || Преподаватель И.О. || Кабинет Площадка
    ...

    Поля можно опускать, если хотите оставить пустыми:
    |||| Предмет |||| Кабинет Площадка

    Возможно перечисление нескольких преподавателей:
    DD.MM || HH:MM || Предмет || Иванов И.И, Фёдоров Ф.Ф., Семёнов О.Е. || Кабинет Площадка

    Если кабинет отсутствует, то его можно опустить:
    DD.MM || HH:MM || Предмет || Иванов И.И, Фёдоров Ф.Ф., Семёнов О.Е. || Площадка

    Можно вписывать год занятий, но он будет игнорироваться. Если нужно его добавить, запросите в Trello.
    DD.MM.YYYY || HH:MM || Предмет || Преподаватель И.О. || Площадка
    """
    template_name = 'admin/extramural_schedule/add_extramural.html'
    render = {
        'description': __doc__,
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
        groups: QuerySet = form.cleaned_data['group']
        schedule_type = form.cleaned_data['schedule_type']

        for date, time, item, teachers, place in form.schedule_fields():
            try:
                day = self.__create_day(date)
                _place = self.__get_place(place)
                _teachers = self.__get_teachers(teachers)

                schedule, _ = ExtramuralSchedule.objects.get_or_create(
                    starts_at=time,
                    ends_at=None,
                    day=day,
                    item_type=ExtramuralSchedule.EMPTY,
                    schedule_type=schedule_type,
                    name=item
                )

                schedule.places.set((_place,))
                schedule.groups.add(*groups)
                schedule.teachers.set(_teachers)
            except Exception as e:
                log.debug(f'Exception was raised. Data:\n{date}\n{time}\n{item}\n{teachers}\n{place}')
                raise e

            count += 1

        ending = 'ы' if count > 1 else ''
        add_message(request, messages.INFO, f'Предмет{ending} успешно добавлены! ({count} шт.)')
        return HttpResponseRedirect('../')

    @staticmethod
    def __create_day(date: Optional[str]) -> Optional[Day]:
        if not date:
            return None

        regex = re.compile(DATE_FORMAT)
        match = regex.match(date)
        day, _ = Day.objects.get_or_create(day=match.group('day'),
                                           month=match.group('month'),
                                           week_day='')
        return day

    @staticmethod
    def __get_place(place: Optional[str]) -> Optional[Place]:
        if not place:
            return None

        regex = re.compile(PLACE_FORMAT)
        match = regex.match(place)
        building = match.group('area') if len(match.groups()) == 2 else ''
        _place, _ = Place.objects.get_or_create(
            number=match.group('cabinet'),
            building=building
        )
        return _place

    @staticmethod
    def __get_teachers(teachers: Tuple[str, ...]) -> Tuple[Optional[Teacher], ...]:
        if not teachers:
            return tuple()

        out: List[Teacher] = []
        regex = re.compile(r'^(?P<lastname>[А-Яа-яЁё]+) (?P<firstname>[А-Яа-яЁё])\.(?P<middlename>[А-Яа-яЁё])\.$')
        for teacher in teachers:
            match = regex.match(teacher)
            _teacher, _ = Teacher.objects.get_or_create(lastname=match.group('lastname'),
                                                        firstname=match.group('firstname'),
                                                        middlename=match.group('middlename'))
            out.append(_teacher)
        return tuple(out)
