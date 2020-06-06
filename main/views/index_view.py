from django.apps import apps
from django.shortcuts import render
from django.views.generic import TemplateView

from schedule.models import Group
from schedule.views import date_block
from main.utils.date import TeachTime
from news.models import News


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        teach_time = TeachTime()
        news: News = apps.get_model(app_label='news', model_name='News')

        return render(request, self.template_name, {
            'date_block': date_block(teach_time),
            'groups': Group.objects.only('name'),
            'latest_news': news.objects.filter(hidden=False).order_by('-date')[:4],
            'teach_state': teach_time.teach_state
        })
