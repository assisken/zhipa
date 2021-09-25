import os

from django.test import TestCase

from schedule.management.scripts.generate import gen_groups_table, gen_teachers_table
from schedule.models import Group, Schedule, Teacher
from smiap.settings import BASE_DIR


class TestExcelDumper(TestCase):
    fixtures = ["groups.json"]

    def setUp(self) -> None:
        self.groups = Group.objects.all()
        self.teachers = Teacher.objects.all()

    def test_group_dump_creates(self):
        path = os.path.join(
            BASE_DIR, "schedule", "tests", "files", "group_template.excel"
        )
        gen_groups_table(self.groups, from_week=1, wb_path=path)

    def test_teacher_dump_creates(self):
        path = os.path.join(
            BASE_DIR, "schedule", "tests", "files", "teacher_template.excel"
        )
        gen_teachers_table(self.teachers, Schedule.STUDY, wb_path=path)
