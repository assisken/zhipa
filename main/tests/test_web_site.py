import json
import os.path

from django.test import TestCase

from smiap.settings import BASE_DIR, BRAND


class TestWebSite(TestCase):
    fixtures = ['groups.json', 'flatpages.json']

    def setUp(self):
        super().setUp()
        with open(os.path.join(BASE_DIR, 'main', 'tests', 'files', 'sitemap.json'), 'r') as file:
            self.urls = json.loads(file.read())

    def test_title(self):
        """Заголовок сайта должен быть как в конфиге"""

        title = f'<title>{BRAND}</title>'
        response = self.client.get('/')
        self.assertInHTML(title, response.content.decode('utf8'))

    def test_sitemap_was_migrated(self):
        """Все старые url-ы должны обрабатываться"""

        for url in self.urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 404, f'Current page: {url}')
