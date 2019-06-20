from django.test import TestCase
from freezegun import freeze_time

from main.models import Group
from main.views.timetable_view import date_block


class ScheduleTest(TestCase):
    @freeze_time('2012-09-03')
    def test_autumn_start(self):
        res = date_block()
        expected = {
            'text': 'Учёба продолжается',
            'num': 2,
            'desc': 'неделя'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    @freeze_time('2016-12-31')
    def test_autumn_end(self):
        res = date_block()
        expected = {
            'text': 'Начало учёбы',
            'num': 9,
            'desc': 'февраля'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    @freeze_time('2016-01-01')
    def test_autumn_end2(self):
        res = date_block()
        expected = {
            'text': 'Начало учёбы',
            'num': 9,
            'desc': 'февраля'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    @freeze_time('2019-02-14')
    def test_spring_start(self):
        res = date_block()
        expected = {
            'text': 'Учёба продолжается',
            'num': 2,
            'desc': 'неделя'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    @freeze_time('2027-07-01')
    def test_spring_end(self):
        res = date_block()
        expected = {
            'text': 'Начало учёбы',
            'num': 1,
            'desc': 'сентября'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')
