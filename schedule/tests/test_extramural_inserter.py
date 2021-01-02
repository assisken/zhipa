from django.test import TestCase
from django.urls import reverse

from main.models import User
from schedule.forms import ExtramuralScheduleForm
from schedule.models import Group, Schedule


class TestExtramuralInserter(TestCase):
    fixtures = ["groups.json"]

    def setUp(self) -> None:
        User.objects.create_superuser(
            username="admin", email="admin@example.com", password="qwerty"
        )
        self.input = """
06.09 13.09 20.09 27.09 04.10 11.10 18.10 25.10||9:00 - 10:30||Иностранный язык||Чалова О.А.||-
||||Философия||Иванов М.А.||-
06.09. 13.09. 20.09||10:45 - 16:15||Дифференциальные уравнения||Абасов Н.М.||-
04.10 18.10 25.10||10:45 - 14:30 10:45 - 14:30 10:45 - 12:15||Математическая логика и теория алгоритмов||Абасов Н.М.||-
17.10 14.11 28.11||14:45 - 18:00 16:30 - 19:45 16:30 - 21:30||Алгоритмические языки и программирование||Антонова А.С.||-
21.09 28.09 05.10 12.10 09.11 16.11||18:15 - 19:45||Теория вероятностей и математическая статистика||Осокин А.В.||-
10.10 07.11||13:00 -18:00 13:00 - 16:15||Базы данных||Квашнин В.М.||-
||||Физика||Каленова Н.В.||-
""".strip()

    def test_several_extramural_are_inserted(self):
        self.client.login(username="admin", password="qwerty")
        form = ExtramuralScheduleForm(
            data={
                "schedule_type": Schedule.STUDY,
                "group": Group.objects.filter(study_form=Group.EXTRAMURAL).first().id,
                "separator": "||",
                "schedule": self.input,
            }
        )
        self.failIf(not form.is_valid(), f"Not valid form:\n{form.errors.as_text()}")

        resp = self.client.post(
            reverse("admin:admin-add-several-extramural"), data=form.data, follow=True
        )
        self.assertEqual(200, resp.status_code)
        self.client.logout()
