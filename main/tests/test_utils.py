from unittest import TestCase

from parameterized import parameterized

from main.utils.date import get_year_from_string


class TestUtils(TestCase):
    @parameterized.expand(
        (
            ("2020", "2020"),
            (
                "Гого-чё – 2018: 3151 Международная молодёжная научная конференция: Сборник тезисов докладов: М.; "
                "Мышинный янтарный университет им. Короля Людовика IX, 2018. Т.5, 123 с., с. 233-233",
                "2018",
            ),
            ("Труды МЯУ. 2017. № 195. ISSN: 5828-5858.", "2017"),
            (
                "Старый Осколок янычара. ТНТ, 201-е издание, переработанное и недополненное, 2018г.",
                "2018",
            ),
        )
    )
    def test_year_from_string(self, string, expect):
        self.assertEqual(expect, get_year_from_string(string))
