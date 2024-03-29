from datetime import datetime

from django.core.paginator import Paginator as OldPaginator
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView

from .models import News


class NewsListView(ListView):
    class Paginator(OldPaginator):
        def get_elided_page_range(self, number=1, *, on_each_side=2, on_ends=1):
            return super().get_elided_page_range(
                number=number, on_each_side=on_each_side, on_ends=on_ends
            )

    model = News
    queryset = News.objects.filter(hidden=False).prefetch_related("newscover")
    paginate_by = 5
    page_kwarg = "number"
    context_object_name = "news_list"
    template_name = "news/list.html"
    paginator_class = Paginator


class NewsDetailView(DetailView):
    model = News
    context_object_name = "news"
    template_name = "news/index.html"

    def get_context_data(self, **kwargs):
        self.object: News
        context = super().get_context_data(**kwargs)
        context["last_news"] = News.objects.filter(hidden=False)[:5]

        return context

    def get(self, request, *args, **kwargs):
        news: News = self.get_object()
        if news.url:
            return redirect("news:news", url=news.url)
        return super().get(request, *args, **kwargs)


class NewsDateListView(ListView):
    model = News
    context_object_name = "news_list"
    template_name = "news/list.html"

    def get_queryset(self):
        return News.objects.filter(hidden=False, **self.kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs["date__year"]
        month = self.kwargs.get("date__month", 1)
        day = self.kwargs.get("date__day", 1)
        date = datetime(year, month, day)
        if day:
            context["news_date"] = f'за {date.strftime("%-d %B %Y")} года'
        elif month:
            context["news_date"] = f'за {date.strftime("%B %Y")} года'
        else:
            context["news_date"] = f'за {date.strftime("%Y")} год'

        return context


class NewsDateDetailView(DetailView):
    model = News
    context_object_name = "news"
    template_name = "news/index.html"

    def get_object(self, queryset: QuerySet = None):
        return get_object_or_404(self.model, **self.kwargs)


class NewsUrlDetailView(DetailView):
    model = News
    context_object_name = "news"
    template_name = "news/index.html"

    def get_object(self, queryset: QuerySet = None):
        kwargs = {
            "url": self.kwargs["url"],
        }
        return get_object_or_404(self.model, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
