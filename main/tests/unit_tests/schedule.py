from datetime import date

from django.test import TestCase
from freezegun import freeze_time

from main.views.timetable_view import date_block
from utils.date import TeachTime


class ScheduleTest(TestCase):
    def test_autumn_start(self):
        res = date_block(TeachTime(date(2012, 9, 3)))
        expected = {
            'text': 'Учёба продолжается',
            'num': 2,
            'desc': 'неделя'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    def test_autumn_end(self):
        res = date_block(TeachTime(date(2016, 12, 31)))
        expected = {
            'text': 'Начало учёбы',
            'num': 9,
            'desc': 'февраля'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    def test_autumn_end2(self):
        res = date_block(TeachTime(date(2016, 1, 1)))
        expected = {
            'text': 'Начало учёбы',
            'num': 9,
            'desc': 'февраля'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    @freeze_time('2019-02-14')
    def test_spring_start(self):
        res = date_block(TeachTime(date.today()))
        expected = {
            'text': 'Учёба продолжается',
            'num': 2,
            'desc': 'неделя'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

    def test_spring_end(self):
        res = date_block(TeachTime(date(2027, 7, 1)))
        expected = {
            'text': 'Начало учёбы',
            'num': 1,
            'desc': 'сентября'
        }
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')
