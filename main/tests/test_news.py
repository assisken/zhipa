from django.test import TestCase
from django.urls import reverse

from main.models import Staff


class UnitTests(TestCase):
    fixtures = ['news.json']

    def test_news_is_shown(self):
        """Петя должен видеть неспрятанные новости"""

        visible = ['На ярмарке продалась шиншила',
                   'Опознан шиншило-генератор!']
        hidden = ['Самая секретная новость на свете!', 'О, нет!']
        url = reverse('news-list-begin')
        response = self.client.get(url)

        for news in visible:
            self.assertContains(
                response, news, msg_prefix='Новость не отображатся. ', html=True
            )
        for news in hidden:
            self.assertNotContains(
                response, news, msg_prefix='Новость не спрятана. ', html=True
            )

    def test_news_url_does_work(self):
        """Новости с URL-ом должны иметь свой url"""

        title = 'На ярмарке продалась шиншила'
        # url = '/materials/news/2000/11/11/test_url'
        url = reverse('news-date-url', kwargs={
            'year': 2000,
            'month': 11,
            'day': 11,
            'url': 'test_url'
        })

        response = self.client.get(url)
        self.assertContains(
            response, title, msg_prefix='Новость не имеет свой URL', html=True
        )
