import json

import requests

from main.models import Group


def fetch_groups(url: str, password: str, department: str) -> None:
    resp = requests.get(url.format(password=password, department=department))
    data = json.loads(resp.content.decode('utf8'))['data']

    for group, value in data.items():
        Group.objects.create(
            name=group,
            semester=int(value['semester']),
            study_form=value['study_form']
        )
