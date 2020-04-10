from django.test import TestCase

from main.models import Publication
from main.utils.date import get_year_from_string


class TestPublications(TestCase):
    fixtures = ['publications.json']

    def test_publications_get_year(self):
        for publication in Publication.objects.all():
            self.assertEqual(get_year_from_string(publication.place), publication.year())
