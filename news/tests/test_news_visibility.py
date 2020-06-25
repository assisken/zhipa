from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized


class TestNewsVisibility(TestCase):
    fixtures = ["news.json"]

    @parameterized.expand(("На ярмарке продалась шиншила",))
    def test_news_visibility(self, title: str):
        url = reverse("news:news-list")
        response = self.client.get(url)

        self.assertContains(response, title, msg_prefix="Новость не отображатся. ")

    @parameterized.expand(("Самая секретная новость на свете!",))
    def test_news_is_hidden(self, title: str):
        url = reverse("news:news-list")
        response = self.client.get(url)

        self.assertNotContains(response, title, msg_prefix="Новость не спрятана. ")
