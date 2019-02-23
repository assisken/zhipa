from django.views.generic import ListView

from main.models import News


class NewsView(ListView):
    model = News
    queryset = News.objects.filter(hidden=False)
    paginate_by = 5
    page_kwarg = 'number'
    context_object_name = 'news_list'
    template_name = 'materials/news/list.html'
