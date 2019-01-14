import logging
from django.shortcuts import render
from django.views.generic import TemplateView, View
from main.schedule.parser import ScheduleParser

from smiap.settings import LOG


class ScheduleIndex(TemplateView):
    groups = ['М3О-133Б-18', 'М3О-233Б-17']
    template_name = "materials/timetable/index.html"

    def get(self, request):
        week = request.GET.get('week', None)
        schedule = ScheduleParser(self.groups[0], week=week)
        LOG.debug(schedule.result)

        return render(request, self.template_name, {
            'week': week,
            'groups': self.groups,
            'schedule': schedule.result
        })
