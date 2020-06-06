from django.core.management import BaseCommand, CommandParser

from schedule.management.scripts import generate


class Command(BaseCommand):
    help = 'Generates an excel extramural_schedule'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--groups',
            action='store_true',
            help='Generate extramural_schedule for groups'
        )
        parser.add_argument(
            '--teachers',
            action='store_true',
            help='Generate extramural_schedule for teachers'
        )

    def handle(self, *args, **options):
        if options['groups']:
            generate.gen_groups_table()
        elif options['teachers']:
            generate.gen_teachers_table()


