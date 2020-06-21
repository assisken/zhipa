from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from jinja2.filters import do_title

from news.models import News, NewsContentImage


class TestNewsContentRender(TestCase):
    fixtures = ['news.json', 'covers.json']

    @parameterized.expand((
        [{}],
        [{'number': 1}],
        [{'date__year': 2000}],
        [{'date__year': 2000, 'date__month': 11}],
        [{'date__year': 2000, 'date__month': 11, 'date__day': 11}],
    ))
    def test_render_news_in_list(self, kwargs):
        url = reverse('news:news-list', kwargs=kwargs)
        news_list = News.objects.prefetch_related('newscover').filter(hidden=False)
        response = self.client.get(url)

        for news in news_list:
            news: News
            self.assertContains(response, news.title)
            self.assertContains(response, news.description)
            self.assertContains(response, news.get_absolute_url())
            self.assertContains(response, do_title(news.date.strftime('%Y')))
            self.assertContains(response, do_title(news.date.strftime('%B')))
            self.assertContains(response, do_title(news.date.strftime('%-d')))
            self.assertContains(response, news.newscover.content)
            self.assertContains(response, news.newscover.color)
            self.assertContains(response, news.newscover.img.url)
            self.assertContains(response, news.newscover)
            self.assertNotContains(response, news.text)
            self.assertNotContains(response, news.hidden)

    @parameterized.expand((
        [{'pk': 1}],
        [{'pk': 2}],
        [{'url': 'test_url'}],
        [{'date__year': 2000, 'date__month': 11, 'date__day': 11, 'url': 'test_url'}],
    ))
    def test_render_news_instance(self, kwargs):
        url = reverse('news:news', kwargs=kwargs)
        news = News.objects.prefetch_related('newscover', 'newscontentimage_set').get(**kwargs)
        response = self.client.get(url, follow=True)

        self.assertContains(response, news.title, msg_prefix=f'Page should contain at {url}')
        self.assertContains(response, news.text, msg_prefix=f'Page should contain at {url}')
        self.assertContains(response, do_title(news.date.strftime('%Y')), msg_prefix=f'Page should contain at {url}')
        self.assertContains(response, do_title(news.date.strftime('%m')), msg_prefix=f'Page should contain at {url}')
        self.assertContains(response, do_title(news.date.strftime('%-d')), msg_prefix=f'Page should contain at {url}')
        self.assertNotContains(response, news.hidden, msg_prefix=f'Page should not contain at {url}')

        for content_image in news.newscontentimage_set.all():
            content_image: NewsContentImage
            self.assertContains(response, content_image.img.url)
            self.assertNotContains(response, content_image.name)
