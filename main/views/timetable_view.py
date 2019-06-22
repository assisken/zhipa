from datetime import datetime, timedelta
from typing import Dict, Union

from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Group
from utils.date import TeachTime, TeachState
from utils.group import course


class TimetableView(TemplateView):
    template_name = "materials/timetable/index.html"

    def get(self, request, *args, **kwargs):
        teach_time = TeachTime()
        groups = Group.objects.only('name')
        group_name = request.GET.get('group', groups.first().name)
        week = request.GET.get('week', teach_time.week if teach_time.week <= teach_time.weeks_in_semester else 1)

        schedule = Group.objects.get(name=group_name).schedule[str(week)]

        if len(groups) > 0:
            schedule = sorted(schedule, key=lambda x: x[0])
            weeks = teach_time.weeks_in_semester
        else:
            weeks = 0

        return render(request, self.template_name, {
            'groups': groups,
            'group_name': group_name,
            'weeks': weeks,
            'week': week,
            'schedule': schedule,
            'date_block': date_block(teach_time),
            'course': course(group_name) if group_name else 0
        })


def date_block(teach_time: TeachTime = TeachTime()):
    teach_state = teach_time.teach_state
    if teach_state.it_is(TeachState.SEMESTER):
        return {
            'text': 'Учёба продолжается',
            'num': teach_time.week,
            'desc': 'неделя'
        }
    elif teach_state.it_is(TeachState.HOLIDAYS):
        return {
            'text': 'Начало учёбы',
            'num': teach_time.next_start.day,
            'desc': teach_time.next_start.strftime('%B')
        }

    return {
        'text': '',
        'num': '404',
        'desc': 'Not Found'
    }
