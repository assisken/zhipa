from datetime import date

from constance.test import override_config
from django.test import TestCase
from django.urls import reverse

from main.utils.date import TeachTime
from schedule.models import FullTimeSchedule, Group
from schedule.views import date_block


class FulltimeScheduleTest(TestCase):
    fixtures = ["groups.json"]

    def setUp(self) -> None:
        self.url_pattern = "{url}?group={group}&week={week}"
        self.groups = Group.objects.filter(study_form=Group.FULL_TIME)

    def test_empty_schedule(self):
        empty_week = "2"
        expect = "На данной неделе занятия по расписанию отсутствуют"

        for group in self.groups:
            url = self.url_pattern.format(
                url=reverse("schedule:timetable"), group=group.name, week=empty_week
            )
            resp = self.client.get(url)
            self.assertContains(
                resp, expect, msg_prefix="Некорректное отображение пустой недели"
            )

    def test_schedule_for_correctness(self):
        week_with_schedule = "1"
        msg = "Некорректно отображается расписание"

        for group in self.groups:
            url = self.url_pattern.format(
                url=reverse("schedule:timetable"),
                group=group.name,
                week=week_with_schedule,
            )
            resp = self.client.get(url)
            schedule = FullTimeSchedule.objects.prefetch_related(
                "group", "teachers"
            ).filter(group=group, hidden=False)
            self.assertContains(
                resp,
                group.name,
                msg_prefix="Не отображается имя группы, либо не та страница",
            )
            self.assertGreater(len(schedule), 0)

            for item in schedule:
                item: FullTimeSchedule
                teachers = ", ".join(map(str, item.teachers.all()))

                self.assertContains(resp, item.date, msg_prefix=msg)
                self.assertContains(resp, item.time, msg_prefix=msg)
                self.assertContains(resp, item.name, msg_prefix=msg)
                self.assertContains(resp, item.item_type, msg_prefix=msg)
                self.assertContains(resp, item.place, msg_prefix=msg)
                self.assertContains(resp, teachers, msg_prefix=msg)

    @override_config(
        AUTUMN_SEMESTER_START=date(2012, 9, 1), SPRING_SEMESTER_START=date(2013, 2, 4),
    )
    def test_date_block_beginning_of_autumn_semester(self):
        res = date_block(TeachTime(date(2012, 9, 3)))
        expected = {"text": "Учёба продолжается", "num": 2, "desc": "неделя"}
        self.assertDictEqual(expected, res, msg="Dicts not equal. ")

    @override_config(
        AUTUMN_SEMESTER_START=date(2016, 9, 1), SPRING_SEMESTER_START=date(2016, 2, 4),
    )
    def test_date_block_last_day_of_year(self):
        res = date_block(TeachTime(date(2016, 12, 31)))
        expected = {"text": "Учёба продолжается", "num": 18, "desc": "неделя"}
        self.assertDictEqual(expected, res, msg="Dicts not equal. ")

    @override_config(
        AUTUMN_SEMESTER_START=date(2015, 9, 1), SPRING_SEMESTER_START=date(2016, 2, 4),
    )
    def test_date_block_first_day_of_year(self):
        res = date_block(TeachTime(date(2016, 1, 1)))
        expected = {"text": "Учёба продолжается", "num": 18, "desc": "неделя"}
        self.assertDictEqual(expected, res, msg="Dicts not equal. ")

    @override_config(
        SPRING_SEMESTER_START=date(2019, 2, 4),
        NEW_YEAR_AUTUMN_SEMESTER_START=date(2019, 5, 31),
    )
    def test_date_block_beginning_of_winter_semester(self):
        res = date_block(TeachTime(date(2019, 2, 14)))
        expected = {"text": "Учёба продолжается", "num": 2, "desc": "неделя"}
        self.assertDictEqual(expected, res, msg="Dicts not equal. ")

    @override_config(
        SPRING_SEMESTER_START=date(2027, 2, 3),
        NEW_YEAR_AUTUMN_SEMESTER_START=date(2027, 9, 1),
    )
    def test_date_block_beginning_of_autumn_semester_in_fart_future(self):
        res = date_block(TeachTime(date(2027, 6, 30)))
        expected = {
            "text": "Начало учёбы",
            "num": 1,
            "desc": "Сентября",
        }
        self.assertDictEqual(expected, res, msg="Dicts not equal. ")

    def test_hidden_schedule_does_not_shows(self):
        week_with_schedule = "2"
        msg = "Спрятанный предмет не должен отображаться на страничке"

        for group in self.groups:
            url = self.url_pattern.format(
                url=reverse("schedule:timetable"),
                group=group.name,
                week=week_with_schedule,
            )
            resp = self.client.get(url)
            schedule = FullTimeSchedule.objects.prefetch_related(
                "group", "teachers"
            ).filter(group=group, hidden=True)
            for item in schedule:
                self.assertNotContains(resp, item.name, msg_prefix=msg)
