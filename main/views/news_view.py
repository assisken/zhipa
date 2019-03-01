from django.views.generic import ListView, DetailView

from main.models import News


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
        context = super().get_context_data(**kwargs)
        context['last_news'] = News.objects.filter(hidden=False)[:5]
        return context
