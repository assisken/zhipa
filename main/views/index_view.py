from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import News, Group
from main.views.timetable_view import date_block
from utils.date import TeachTime


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        teach_time = TeachTime()

        return render(request, self.template_name, {
            'date_block': date_block(teach_time),
            'groups': Group.objects.only('name'),
            'latest_news': News.objects.filter(hidden=False).order_by('-date')[:4],
            'teach_state': teach_time.teach_state
        })
