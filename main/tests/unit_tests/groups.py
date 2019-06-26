import json
from unittest.mock import patch

from django.test import TestCase
from requests import Response

from main.management.scripts.groups import fetch_groups
from main.models import Group

RESPONSE = {
    'data': {
        '7-БО1-37Б-31': {
            'group_name': '7-БО1-37Б-31',
            'semester': '6',
            'study_form': 'очная'
        },
        '3-БО3-45Б-19': {
            'group_name': '3-БО3-45Б-19',
            'semester': '8',
            'study_form': 'заочная'
        },
    }

}


class MockedResponce(Response):
    def __init__(self, content: str, code: int):
        super().__init__()
        self.status_code = code
        self._content = content.encode('utf8')

    @property
    def content(self):
        return self._content


def mocked_group_response(*args, **kwargs):
    return MockedResponce(json.dumps(RESPONSE), 200)


class GroupTest(TestCase):
    @patch('requests.get', side_effect=mocked_group_response)
    def test_group_fetch(self, mock_get):
        fetch_groups('http://example.com', '', '')
        for group in Group.objects.only('name'):
            self.assertIn(group.name, RESPONSE['data'].keys())
