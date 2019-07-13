import json
import os
from typing import List, Dict

from django.core.management import BaseCommand, CommandParser

from main.models import News, Staff
from smiap.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Imports data from previous database. Use flag `--file` to specify filename. Default is `data.json`'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--file',
            action='store',
            help='Specify file name. Default is `data.json`'
        )

    def handle(self, *args, **options):
        file = options.get('file') or 'data.json'
        path = os.path.join(BASE_DIR, 'import', file)

        try:
            with open(path, 'r') as f:
                raw_data = f.read()
        except FileNotFoundError:
            print('File not found. Please, specify it using flag `--file` or rename it to `data.json`.')
            exit(1)

        data = json.loads(raw_data)

        for item in data:
            name = item.get('name', None)
            if not name:
                continue
            elif name == 'news':
                insert_news(item['data'])
            elif name == 'staff':
                insert_staff(item['data'])

        print('Done successfully!')


def insert_news(data: List[Dict]):
    for news in data:
        image = news['img']
        if image:
            image = image.replace('img', 'images')

        News.objects.create(
            pk=news['id'],
            title=news['title'],
            date=news['date'],
            url=news['url'],
            img=image,
            description=news['description'],
            text=news['text'],
            hidden=news['hidden'],
        )


def insert_staff(data: List[Dict]):
    for staff in data:
        image = staff['img']
        if image:
            image = image.replace('img', 'images')

        Staff.objects.create(
            pk=staff['id'],
            lastname=staff['lastname'],
            firstname=staff['firstname'],
            middlename=staff['patronymic'],
            img=image,
            regalia=staff['regalia'],
            description=staff['description'],
            leader=staff['leader'],
            lecturer=staff['lecturer'],
            hide=staff['hide'],
        )
