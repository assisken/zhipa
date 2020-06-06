import locale
from datetime import date

from django.test import TestCase
from django.urls import reverse

from schedule.models import Group, FullTimeSchedule
from schedule.views import date_block
from main.utils.date import TeachTime


class ScheduleTest(TestCase):
    fixtures = ['groups.json']

    def setUp(self) -> None:
        self.url_pattern = '{url}?group={group}&week={week}'
        self.groups = Group.objects.all()

    def test_empty_schedule(self):
        empty_week = '2'
        expect = 'На данной неделе занятия по расписанию отсутствуют'

        for group in self.groups:
            url = self.url_pattern.format(url=reverse('schedule:timetable'), group=group.name, week=empty_week)
            resp = self.client.get(url)
            self.assertContains(resp, expect, msg_prefix='Некорректное отображение пустой недели')

    def test_schedule_for_correctness(self):
        week_with_schedule = '1'
        msg = 'Некорректно отображается расписание'

        for group in self.groups:
            url = self.url_pattern.format(url=reverse('schedule:timetable'), group=group.name, week=week_with_schedule)
            resp = self.client.get(url)
            schedule = FullTimeSchedule.objects.prefetch_related('day', 'group', 'teachers', 'places') \
                .filter(group=group)
            self.assertContains(resp, '&emsp; {} &emsp;'.format(group.name),
                                msg_prefix='Не отображается имя группы, либо не та страница')
            self.assertGreater(len(schedule), 0)

            for item in schedule:
                item: FullTimeSchedule
                starts_at = item.starts_at.strftime('%H:%M')
                ends_at = item.ends_at.strftime('%H:%M')
                teachers = ', '.join(map(str, item.teachers.all()))
                places = ', '.join(map(str, item.places.all()))

                self.assertContains(resp, item.day.day, msg_prefix=msg)
                self.assertContains(resp, item.day.month, msg_prefix=msg)
                self.assertContains(resp, item.day.week_day, msg_prefix=msg)
                self.assertContains(resp, starts_at, msg_prefix=msg)
                self.assertContains(resp, ends_at, msg_prefix=msg)
                self.assertContains(resp, item.name, msg_prefix=msg)
                self.assertContains(resp, item.item_type, msg_prefix=msg)
                self.assertContains(resp, teachers, msg_prefix=msg)
                self.assertContains(resp, places, msg_prefix=msg)

    def test_date_block(self):
        res = date_block(TeachTime(date(2012, 9, 3)))
        expected = {'text': 'Учёба продолжается', 'num': 2, 'desc': 'неделя'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2016, 12, 31)))
        expected = {'text': 'Учёба продолжается', 'num': 18, 'desc': 'неделя'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2016, 1, 1)))
        expected = {'text': 'Учёба продолжается', 'num': 18, 'desc': 'неделя'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2019, 2, 14)))
        expected = {'text': 'Учёба продолжается', 'num': 2, 'desc': 'неделя'}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')

        res = date_block(TeachTime(date(2027, 7, 1)))
        expected = {'text': 'Начало учёбы', 'num': 1, 'desc': locale.nl_langinfo(locale.MON_9)}
        self.assertDictEqual(expected, res, msg='Dicts not equal. ')
