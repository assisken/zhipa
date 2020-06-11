from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from news.models import News
from news.views import NewsListView


class TestNewsUrls(TestCase):
    fixtures = ['news.json']

    def setUp(self) -> None:
        self.pagination = NewsListView.paginate_by

    @parameterized.expand((
        [{}],
        [{'number': 1}],
        [{'date__year': 2000}],
        [{'date__year': 2000, 'date__month': 11}],
        [{'date__year': 2000, 'date__month': 11, 'date__day': 11}],
    ))
    def test_several_news_render(self, kwargs):
        url = reverse('news:news-list', kwargs=kwargs)
        titles = News.objects.filter(hidden=False).values_list('title', flat=True).order_by('-id')[:self.pagination]
        response = self.client.get(url)
        for title in titles:
            self.assertContains(response, title, msg_prefix=f'Title {title} was not found at url: {url}')

    @parameterized.expand((
        [{'pk': 1}],
        [{'pk': 2}],
        [{'url': 'test_url'}],
        [{'date__year': 2000, 'date__month': 11, 'date__day': 11, 'url': 'test_url'}],
    ))
    def test_news_instance_renders(self, kwargs):
        title = News.objects.values_list('title', flat=True).get(**kwargs)
        url = reverse('news:news', kwargs=kwargs)
        response = self.client.get(url, follow=True)
        self.assertContains(response, title)
