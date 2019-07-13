import json
import os
from datetime import datetime
from pprint import pprint

from django.test import TestCase
from django.utils.timezone import make_aware
from pytz import timezone

from main.management.scripts.file_import import handle_data
from main.models import News, Staff
from smiap.settings import BASE_DIR, TIME_ZONE


class TestImportCommand(TestCase):
    def setUp(self) -> None:
        with open(os.path.join(BASE_DIR, 'main', 'tests', 'files', 'data.json'), 'r') as file:
            raw_data = file.read()

        self.data = json.loads(raw_data)
        self.expected_news = [
            News(
                pk=44,
                title='Заголовок2',
                date=make_aware(
                    datetime.strptime('2019-05-29 12:32:12', '%Y-%m-%d %H:%M:%S'),
                    timezone=timezone(TIME_ZONE)
                ),
                url='test',
                img='images/news/null/cover.jpg',
                description='spsh',
                hidden=True
            ),
            News(
                pk=18,
                title='Заголовок',
                date=make_aware(
                    datetime.strptime('2015-11-21 00:00:00', '%Y-%m-%d %H:%M:%S'),
                    timezone=timezone(TIME_ZONE)
                ),
                url='',
                img='images/news/no/cover.jpg',
                description=':DDDD',
                text='benis',
                hidden=False
            )
        ]
        self.expected_staff = [
            Staff(
                pk=1,
                lastname='Пупкин',
                firstname='Вася',
                middlename='Петрович',
                img='img/people/pupkin.jpg',
                regalia='Самый старший',
                description='Просто описание...',
                leader=True,
                lecturer=True,
                hide=False,
            ),
            Staff(
                pk=8,
                lastname='Стешняшко',
                firstname='Константин',
                middlename='Ильич',
                img=None,
                regalia='Старший',
                description='Работает стоя',
                leader=False,
                lecturer=True,
                hide=False,
            ),
            Staff(
                pk=36,
                lastname='Петров',
                firstname='Антон',
                middlename='Борисович',
                img='img/people/petrov.jpg',
                regalia='Младший',
                description=None,
                leader=False,
                lecturer=False,
                hide=True,
            ),
        ]

    def test_handle_data(self):
        handle_data(self.data)
        self.assertListEqual(list(News.objects.all()), self.expected_news)
        self.assertListEqual(list(Staff.objects.all()), self.expected_staff)
