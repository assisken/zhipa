from datetime import datetime, timedelta
from typing import Dict, Union

from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Group


class TimetableView(TemplateView):
    template_name = "materials/timetable/index.html"

    def get(self, request, *args, **kwargs):
        groups = Group.objects.only('name')
        group_name = request.GET.get('group', None)
        week = request.GET.get('week', '1')

        if group_name:
            group = Group.objects.get(name=group_name)
        else:
            now = datetime.now()
            year = now.year % 100
            if now.month < 9:
                year -= 1
            group = Group.objects.filter(name__endswith=year).first()

        if len(groups) > 0:
            schedule = sorted(group.schedule[week], key=lambda x: x[0])
            weeks = group.weeks()
            course = group.course()
        else:
            schedule = []
            weeks = 0
            course = 0

        return render(request, self.template_name, {
            'groups': groups,
            'group': group,
            'weeks': weeks,
            'week': week,
            'schedule': schedule,
            'date_block': date_block(),
            'course': course
        })


def date_block() -> Dict[str, Union[int, str]]:
    now = datetime.now()

    def current_week(date: datetime):
        return now.isocalendar()[1] - date.isocalendar()[1] + 1

    def avoid_sunday(date):
        return date + timedelta(days=1) if date.weekday() == 6 else date

    if now.month >= 9:
        autumn_start1 = avoid_sunday(datetime(year=now.year, month=9, day=1))
        spring_start = avoid_sunday(datetime(year=now.year + 1, month=2, day=9))
        autumn_start2 = avoid_sunday(datetime(year=now.year + 1, month=9, day=1))
    else:
        autumn_start1 = avoid_sunday(datetime(year=now.year - 1, month=9, day=1))
        spring_start = avoid_sunday(datetime(year=now.year, month=2, day=9))
        autumn_start2 = avoid_sunday(datetime(year=now.year, month=9, day=1))

    autumn_end = autumn_start1 + timedelta(days=7 * 17)
    spring_end = spring_start + timedelta(days=7 * 17)

    if autumn_start1 <= now < autumn_end:
        return {
            'text': 'Учёба продолжается',
            'num': current_week(autumn_start1),
            'desc': 'неделя'
        }
    elif autumn_end <= now < spring_start:
        return {
            'text': 'Начало учёбы',
            'num': spring_start.day,
            'desc': spring_start.strftime('%B')
        }
    elif spring_start <= now < spring_end:
        return {
            'text': 'Учёба продолжается',
            'num': current_week(spring_start),
            'desc': 'неделя'
        }
    elif spring_end <= now < autumn_start2:
        return {
            'text': 'Начало учёбы',
            'num': autumn_start2.day,
            'desc': autumn_start2.strftime('%B')
        }

    return {
        'text': '',
        'num': '404',
        'desc': 'Not Found'
    }
