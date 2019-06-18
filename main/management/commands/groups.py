from time import sleep

from django.core.management import BaseCommand, CommandParser

import json
from requests import get, HTTPError

from main.management.scripts.schedule import parse_schedule_for
from main.models import Group
from smiap.settings import LMS_PASSWORD


class Command(BaseCommand):
    help = 'Manipulates with database groups'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--lms',
            action='store_true',
            help='Get groups from lms'
        )
        parser.add_argument(
            '--schedule',
            action='store_true',
            help='Get schedule from mai'
        )

    def handle(self, *args, **options):
        if options['lms']:
            resp = get(f'http://lms.mai.ru/blocks/iis/316.php?pwd={LMS_PASSWORD}&department=316')
            _json = json.loads(resp.content.decode('utf8'))
            groups = list(_json['data'])
            for group in groups:
                Group.objects.create(name=group)
        elif options['schedule']:
            groups = Group.objects.all()
            for group in groups:
                print('Parsing group {}...'.format(group.name))
                group.schedule = parse_schedule_for(group.name)
                group.save()
        print('Done!')
