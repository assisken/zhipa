import json
import os

from django.core.management import BaseCommand, CommandParser
from termcolor import cprint

from main.management.scripts.file_import import handle_data
from smiap.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Imports data from previous database. Use flag `--file` to specify filename. Default is `data.json`'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--file',
            action='store',
            help='Specify file name. Default is `data.json`',
            default='data.json'
        )

    def handle(self, *args, **options):
        cprint('Importing data file...', attrs=['bold', 'underline'])

        file = options.get('file')
        path = os.path.join(BASE_DIR, 'import', file)

        try:
            with open(path, 'r') as f:
                raw_data = f.read()
        except FileNotFoundError:
            print('File not found. Please, specify it using flag `--file` or rename it to `data.json`.')
            exit(1)

        data = json.loads(raw_data)
        handle_data(data)

        print('Done successfully!')
