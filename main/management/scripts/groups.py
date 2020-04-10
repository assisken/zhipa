import csv
import json
import os

import requests
from django.db import IntegrityError

from main.models import Group
from smiap.settings import BASE_DIR
from main.utils.exceptions import LmsDoesNotRespondError, LmsRespondsAnEmptyListError


def fetch_groups(url_pattern: str, password: str, department: str) -> None:
    url = url_pattern.format(password=password, department=department)
    resp = requests.get(url)

    if resp.status_code not in (200, 500):
        raise LmsDoesNotRespondError(url)

    data = json.loads(resp.content.decode('utf8'))['data']
    if not data:
        raise LmsRespondsAnEmptyListError(url)

    for group, value in data.items():
        try:
            Group.objects.create(
                name=group,
                semester=int(value['semester']),
                study_form=value['study_form']
            )
        except IntegrityError:
            print('Group {} is already exist! Skipping...'.format(group))


def fetch_groups_from_csv(file_name: str):
    path = os.path.join(BASE_DIR, 'import', file_name)
    with open(path, 'r', newline='\n') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            try:
                Group.objects.create(
                    name=row[0],
                    semester=int(row[1])
                )
            except IntegrityError:
                print('Group {} is already exist! Skipping...'.format(row[0]))
