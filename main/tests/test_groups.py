import json
import sys

from io import StringIO
from typing import Any
from unittest.mock import patch, Mock

from django.test import TestCase

from main.management.scripts.groups import fetch_groups
from main.models import Group
from utils.exceptions import LmsDoesNotRespondError

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


def mocked_404_respond(*args, **kwargs):
    resp = Mock()
    resp.status_code = 404
    return resp


class GroupTest(TestCase):
    def setUp(self) -> None:
        self.url = 'http://example.com/'

    @patch('requests.get', side_effect=mocked_group_response)
    def test_group_fetch(self, mock_request: Any):
        fetch_groups(self.url, '', '')
        mock_request.assert_called_with(self.url)
        for group in Group.objects.only('name'):
            self.assertIn(group.name, RESPONSE['data'].keys())

    @patch('requests.get')
    def test_handle_lms_respond_404(self, mock_request: Any):
        capture = StringIO()
        sys.stdout = capture

        with self.assertRaises(LmsDoesNotRespondError):
            fetch_groups(self.url, '', '')
