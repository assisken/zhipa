from django.test import TestCase
from django.urls import reverse

from main.models import Staff


class UnitTests(TestCase):
    fixtures = ['staff.json']

    def setUp(self):
        pass

    def test_staff_is_shown(self):
        """На сайте должны отображаться все нескрытые сотрудники"""

        url = reverse('staff')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Doesn't work with Jinja2 :(
        # self.assertTemplateUsed(response=response, template_name='about/staff.html')

        staff = Staff.objects.filter(hide=False)
        for s in staff:
            self.assertIn(str(s), response.content.decode('utf-8'))
