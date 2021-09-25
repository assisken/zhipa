import os

from django.test import TestCase

from schedule.management.scripts.generate import (
    Config,
    gen_groups_table,
    gen_teachers_table,
)
from schedule.models import Group, Schedule, Teacher
from smiap.settings import BASE_DIR


class TestExcelDumper(TestCase):
    fixtures = ["groups.json"]

    def setUp(self) -> None:
        self.groups = Group.objects.all()
        self.teachers = Teacher.objects.all()

    def test_group_dump_creates(self):
        path = os.path.join(
            BASE_DIR, "schedule", "tests", "files", "group_template.xlsx"
        )
        config = Config(
            template_path=path,
            from_week=1,
            to_week=2,
            print_item_name=True,
            print_item_type=True,
            print_places=True,
        )
        gen_groups_table(self.groups, config)

    def test_teacher_dump_creates(self):
        path = os.path.join(
            BASE_DIR, "schedule", "tests", "files", "teacher_template.xlsx"
        )
        config = Config(
            template_path=path,
            from_week=1,
            to_week=2,
            print_item_name=True,
            print_item_type=True,
            print_places=True,
            schedule_type=Schedule.STUDY,
        )
        gen_teachers_table(self.teachers, config)
