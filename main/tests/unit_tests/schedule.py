from datetime import date
from typing import List, Dict, Any

from django.test import TestCase
from django.urls import reverse

from main.models import Group
from main.views.timetable_view import date_block
from utils.date import TeachTime


class ScheduleTest(TestCase):
    fixtures = ['groups.json']

    def setUp(self) -> None:
        self.url_pattern = '{url}?group={group}&week={week}'
        self.groups = Group.objects.all()

    def test_empty_schedule(self):
        empty_week = '2'
        expect = 'На данной неделе занятия по расписанию отсутствуют'

        for group in self.groups:
            url = self.url_pattern.format(url=reverse('timetable'), group=group.name, week=empty_week)
            resp = self.client.get(url)
            self.assertContains(resp, expect, msg_prefix='Некорректное отображение пустой недели')

    def test_schedule_for_correctness(self):
        week_with_schedule = '1'
        msg = 'Некорректно отображается расписание'

        for group in self.groups:
            url = self.url_pattern.format(url=reverse('timetable'), group=group.name, week=week_with_schedule)
            resp = self.client.get(url)
            week = group.schedule[week_with_schedule]

            for day in week:
                date: str = day[0]
                day_name: str = day[1]
                items: List[Any] = day[2]
                self.assertContains(resp, date, msg_prefix=msg)
                self.assertContains(resp, day_name, msg_prefix=msg)
                for item in items:
                    time: str = item[0]
                    abbrev: str = item[1]
                    item_name: str = item[2]
                    place: Dict[str, str] = item[3]['place']
                    auditory: Dict[str, str] = item[3]['auditory']
                    teachers: List[str] = item[4]

                    self.assertContains(resp, time, msg_prefix=msg)
                    self.assertContains(resp, abbrev, msg_prefix=msg)
                    self.assertContains(resp, item_name, msg_prefix=msg)
                    self.assertContains(resp, place, msg_prefix=msg)
                    self.assertContains(resp, auditory, msg_prefix=msg)
                    self.assertContains(resp, ' '.join(teachers), msg_prefix=msg)

    def test_date_block(self):
        res = date_block(TeachTime(date(2012, 9, 3)))
        expected = {'text': 'Учёба продолжается', 'num': 2, 'desc': 'неделя'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2016, 12, 31)))
        expected = {'text': 'Начало учёбы', 'num': 9, 'desc': 'февраля'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2016, 1, 1)))
        expected = {'text': 'Начало учёбы', 'num': 9, 'desc': 'февраля'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2019, 2, 14)))
        expected = {'text': 'Учёба продолжается', 'num': 2, 'desc': 'неделя'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2027, 7, 1)))
        expected = {'text': 'Начало учёбы', 'num': 1, 'desc': 'сентября'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')
