import json
from typing import Any
from unittest.mock import patch, Mock

from django.test import TestCase

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


def mocked_group_response(*args, **kwargs):
    resp = Mock()
    resp.status_code = 200
    resp.content = json.dumps(RESPONSE).encode('utf8')
    return resp


class GroupTest(TestCase):
    @patch('requests.get', side_effect=mocked_group_response)
    def test_group_fetch(self, mock_request: Any):
        url = 'http://example.com/'
        fetch_groups(url, '', '')
        mock_request.assert_called_with(url)
        for group in Group.objects.only('name'):
            self.assertIn(group.name, RESPONSE['data'].keys())
