from django.core.management.base import BaseCommand, CommandParser

import main.management.scripts.dump as dump


class Command(BaseCommand):
    help = 'Dumps specified data'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            '--news',
            action='store_true',
            help='Dumps news'
        )
        parser.add_argument(
            '--staff',
            action='store_true',
            help='Dumps staff'
        )

    def handle(self, *args, **options):
        if options['news']:
            news = [dump.gen_normal_news(news)
                    for news in dump.iter_news()]
            dump.write_to_file(news)

        elif options['staff']:
            staffs = [dump.gen_normal_staff(staff)
                      for staff in dump.iter_staff()]
            dump.write_to_file(staffs)
