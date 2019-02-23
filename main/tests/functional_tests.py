import json
import os.path

from django.test import LiveServerTestCase
from selenium.webdriver import Chrome, ChromeOptions

from smiap.settings import CONFIG, BASE_DIR


class TestWebSite(LiveServerTestCase):
    def setUp(self):
        options = ChromeOptions()
        options.set_headless(True)
        self.browser = Chrome(options=options)

        with open(os.path.join(BASE_DIR, 'main', 'tests', 'files', 'sitemap.json'), 'r') as file:
            self.urls = json.loads(file.read())

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        """Заголовок сайта должен быть как в конфиге"""

        title = CONFIG.get('brand', 'name')
        self.browser.get(self.live_server_url)
        self.assertIn(self.browser.title, title)

    def test_sitemap_was_migrated(self):
        """Все старые url-ы должны обрабатываться"""

        for url in self.urls:
            response = self.client.get(self.live_server_url + url)
            self.assertNotEqual(response.status_code, 404, f'Current page: {url}')
