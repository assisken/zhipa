from django.test import TestCase
from django.urls import reverse

from main.models import Staff


class UnitTests(TestCase):
    fixtures = ['staff.json', 'news.json']

    def test_staff_is_shown(self):
        """Петя должен видеть всех нескрытые сотрудники"""

        url = reverse('staff')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Doesn't work with Jinja2 :(
        # self.assertTemplateUsed(response=response, template_name='about/staff.html')

        staff = Staff.objects.filter(hide=False)
        for s in staff:
            self.assertIn(str(s), response.content.decode('utf-8'))

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
