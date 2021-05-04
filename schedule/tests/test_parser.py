import os

from django.test import TestCase

from schedule.management.scripts.schedule import Item, parse_schedule
from smiap.settings import BASE_DIR


class TestParser(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        with open(
            os.path.join(BASE_DIR, "schedule", "tests", "files", "schedule.html"), "r"
        ) as file:
            self.schedule_body = file.read()
        with open(
            os.path.join(
                BASE_DIR, "schedule", "tests", "files", "session_schedule.html"
            ),
            "r",
        ) as file:
            self.session_body = file.read()
        self.schedule = [
            Item(
                date="23.12",
                week_day="Ср",
                time="13:00 – 14:30",
                type="ПЗ",
                title="Правоведение",
                place="Орш. А-318",
                teachers=[],
            ),
            Item(
                date="23.12",
                week_day="Ср",
                time="14:45 – 16:15",
                type="ЛК",
                title="Правоведение",
                place="Орш. В-501",
                teachers=["Калита Владимир Николаевич"],
            ),
            Item(
                date="24.12",
                week_day="Чт",
                time="13:00 – 14:30",
                type="ПЗ",
                title="Линейная алгебра и аналитическая геометрия",
                place="Орш. А-424",
                teachers=["Абасов Нариман Магамедович"],
            ),
            Item(
                date="24.12",
                week_day="Чт",
                time="14:45 – 16:15",
                type="ПЗ",
                title="Физическая культура",
                place="--стадион",
                teachers=[],
            ),
            Item(
                date="26.12",
                week_day="Сб",
                time="13:00 – 14:30",
                type="ЛК",
                title="Информатика",
                place="Орш. В-414",
                teachers=["Викулин Максим Александрович"],
            ),
            Item(
                date="26.12",
                week_day="Сб",
                time="14:45 – 16:15",
                type="ПЗ",
                title="Физическая культура",
                place="--стадион",
                teachers=[],
            ),
            Item(
                date="28.12",
                week_day="Пн",
                time="14:45 – 16:15",
                type="ЛК",
                title="Введение в специальность",
                place="Берн. 14-623",
                teachers=["Цырков Георгий Александрович"],
            ),
            Item(
                date="29.12",
                week_day="Вт",
                time="09:00 – 10:30",
                type="ПЗ",
                title="Математический анализ",
                place="Орш. В-326",
                teachers=[],
            ),
            Item(
                date="29.12",
                week_day="Вт",
                time="13:00 – 14:30",
                type="ПЗ",
                title="Иностранный язык",
                place="Орш. В-502 | --каф.",
                teachers=["Неверова Наталия Викторовна", "Рыбакова Людмила Викторовна"],
            ),
            Item(
                date="29.12",
                week_day="Вт",
                time="14:45 – 16:15",
                type="ПЗ",
                title="Иностранный язык",
                place="Орш. В-508 | --каф.",
                teachers=["Неверова Наталия Викторовна", "Рыбакова Людмила Викторовна"],
            ),
            Item(
                date="30.12",
                week_day="Ср",
                time="14:45 – 16:15",
                type="ЛК",
                title="Русский язык и культура речи",
                place="Орш. В-501",
                teachers=[],
            ),
        ]
        self.session = [
            Item(
                date="16.01",
                week_day="",
                time="13:00 – 14:30",
                type="Экзамен",
                title="Информатика",
                place="Орш. В-414",
                teachers=["Герасимова Ирина Николаевна"],
            ),
            Item(
                date="16.01",
                week_day="",
                time="14:45 – 16:15",
                type="Экзамен",
                title="Информатика",
                place="Орш. В-414",
                teachers=["Герасимова Ирина Николаевна"],
            ),
            Item(
                date="19.01",
                week_day="",
                time="13:00 – 14:30",
                type="Экзамен",
                title="Линейная алгебра и аналитическая геометрия",
                place="Орш. Б-304",
                teachers=["Михайлов Юрий Альбертович"],
            ),
            Item(
                date="19.01",
                week_day="",
                time="14:45 – 16:15",
                type="Экзамен",
                title="Линейная алгебра и аналитическая геометрия",
                place="Орш. Б-304",
                teachers=["Михайлов Юрий Альбертович"],
            ),
        ]

    def test_parse_schedule(self):
        self.assertSequenceEqual(
            self.schedule,
            parse_schedule(self.schedule_body),
        )

    def test_parse_session_schedule(self):
        self.assertSequenceEqual(
            self.session,
            parse_schedule(self.session_body),
        )
