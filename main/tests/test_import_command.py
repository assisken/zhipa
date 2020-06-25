import json
import os
from datetime import datetime
from typing import Type

from django.apps import apps
from django.test import TransactionTestCase
from django.utils.timezone import make_aware
from pytz import timezone

from main.management.scripts.file_import import handle_data
from main.models import Staff
from news.models import News
from smiap.settings import BASE_DIR, TIME_ZONE

_News: Type[News] = apps.get_model("news", "News")


class TestImportCommand(TransactionTestCase):
    def setUp(self) -> None:
        with open(
            os.path.join(BASE_DIR, "main", "tests", "files", "data.json"), "r"
        ) as file:
            raw_data = file.read()

        self.data = json.loads(raw_data)
        self.expected_news = [
            News(
                pk=5,
                title="Заголовок",
                date=make_aware(
                    datetime.strptime("2015-11-21 00:00:00", "%Y-%m-%d %H:%M:%S"),
                    timezone=timezone(TIME_ZONE),
                ),
                url="",
                cover="images/news/no/cover.jpg",
                description=":DDDD",
                text="benis",
                hidden=False,
                render_in="html",
            ),
            News(
                pk=6,
                title="Заголовок2",
                date=make_aware(
                    datetime.strptime("2019-05-29 12:32:12", "%Y-%m-%d %H:%M:%S"),
                    timezone=timezone(TIME_ZONE),
                ),
                url="test",
                cover="images/news/null/cover.jpg",
                description="spsh",
                hidden=True,
                render_in="html",
            ),
        ]
        self.expected_staff = [
            Staff(
                pk=3,
                lastname="Пупкин",
                firstname="Вася",
                middlename="Петрович",
                img="img/people/pupkin.jpg",
                regalia="Самый старший",
                description="Просто описание...",
                leader=True,
                lecturer=True,
                hide=False,
            ),
            Staff(
                pk=4,
                lastname="Стешняшко",
                firstname="Константин",
                middlename="Ильич",
                img=None,
                regalia="Старший",
                description="Работает стоя",
                leader=False,
                lecturer=True,
                hide=False,
            ),
            Staff(
                pk=5,
                lastname="Петров",
                firstname="Антон",
                middlename="Борисович",
                img="img/people/petrov.jpg",
                regalia="Младший",
                description=None,
                leader=False,
                lecturer=False,
                hide=True,
            ),
        ]

    def test_handle_data(self):
        handle_data(self.data)
        result_news = list(_News.objects.order_by("pk").all())
        result_staff = list(Staff.objects.order_by("pk").all())
        self.assertListEqual(result_news, self.expected_news)
        self.assertListEqual(result_staff, self.expected_staff)
