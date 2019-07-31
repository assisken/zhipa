import json

import requests
from django.db import IntegrityError

from main.models import Group


def fetch_groups(url_pattern: str, password: str, department: str) -> None:
    url = url_pattern.format(password=password, department=department)
    resp = requests.get(url)

    if resp.status_code not in (200, 500):
        print('Seems like lms does not response with 200 code.')
        print('Please, update website url or check that website does respond on url:')
        print(url)
        exit(1)

    data = json.loads(resp.content.decode('utf8'))['data']

    for group, value in data.items():
        try:
            Group.objects.create(
                name=group,
                semester=int(value['semester']),
                study_form=value['study_form']
            )
        except IntegrityError:
            print('Group {} is already exist! Skipping...'.format(group))
