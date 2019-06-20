from datetime import datetime, timedelta
from typing import Dict, Union

from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Group
from utils.date import date_block
from utils.group import course


class TimetableView(TemplateView):
    template_name = "materials/timetable/index.html"

    def get(self, request, *args, **kwargs):
        groups = Group.objects.only('name')
        group_name = request.GET.get('group', groups.first().name)
        week = request.GET.get('week', '1')

        schedule = Group.objects.get(name=group_name).schedule[week]

        if len(groups) > 0:
            schedule = sorted(schedule, key=lambda x: x[0])
            weeks = 17
        else:
            weeks = 0

        return render(request, self.template_name, {
            'groups': groups,
            'group_name': group_name,
            'weeks': weeks,
            'week': week,
            'schedule': schedule,
            'date_block': date_block(),
            'course': course(group_name) if group_name else 0
        })
