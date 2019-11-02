from calendar import month_abbr
from datetime import datetime

from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, View

from main.models import News, NewsContentImage
from smiap.settings import DEFAULT_IMG
from utils.news_md_to_html import MD


class NewsListView(ListView):
    model = News
    queryset = News.objects.filter(hidden=False)
    paginate_by = 5
    page_kwarg = 'number'
    context_object_name = 'news_list'
    template_name = 'materials/news/list.html'


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'materials/news/index.html'

    def get_context_data(self, **kwargs):
        self.object: News
        context = super().get_context_data(**kwargs)
        context['last_news'] = News.objects.filter(hidden=False)[:5]

        content = MD(self.object.text) if self.object.render_in == self.object.MARKDOWN else self.object.text

        attachments = NewsContentImage.objects.filter(news=self.object)
        replacing_images = {}
        for a in attachments:
            replacing_images[a.name] = a.img.url if a.img else DEFAULT_IMG
        content = content.format(**replacing_images)
        context['content'] = content

        return context


class NewsDateListView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'materials/news/list.html'

    def get_queryset(self):
        kwargs = {
            'date__year': self.kwargs['year']
        }
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        if month:
            kwargs['date__month'] = month
        if day:
            kwargs['date__day'] = day

        return News.objects.filter(hidden=False, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs.get('month', 1)
        day = self.kwargs.get('day', 1)
        date = datetime(year, month, day)
        if day:
            context['news_date'] = f'за {date.strftime("%-d %B %Y")} года'
        elif month:
            context['news_date'] = f'за {date.strftime("%B %Y")} года'
        else:
            context['news_date'] = f'за {date.strftime("%Y")} год'

        return context


class NewsDateDetailView(DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'materials/news/index.html'

    def get_object(self, queryset: QuerySet=None):
        kwargs = {
            'date__year': self.kwargs['year'],
            'date__month': self.kwargs['month'],
            'date__day': self.kwargs['day'],
            'url': self.kwargs['url'],
        }
        return get_object_or_404(self.model, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        url = self.kwargs['url']

        return context
