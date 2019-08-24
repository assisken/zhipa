from django.core.management import BaseCommand, CommandParser
from termcolor import cprint

from main.management.scripts.groups import fetch_groups
from main.management.scripts.schedule import parse_schedule_for
from main.models import Group
from smiap.settings import LMS_PASSWORD, LMS_URL, DEPARTMENT
from utils.exceptions import LmsDoesNotRespondError, LmsRespondsAnEmptyListError


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
            cprint('Adding student groups...', attrs=['bold', 'underline'])
            try:
                fetch_groups(LMS_URL, LMS_PASSWORD, DEPARTMENT)
            except LmsDoesNotRespondError as e:
                cprint('Seems like lms does not response with 200 code.', attrs=['bold', 'underline'])
                print('Please, update website url or check that website does respond on url:')
                print(e.args[0])
            except LmsRespondsAnEmptyListError as e:
                cprint('Lms responds an empty list, null or false that does not correct.', 'red', attrs=['bold'])
                print('Please, check url and call with developers or administration.')
                print(e.args[0])
            else:
                print('Done!')

        elif options['schedule']:
            cprint('Parsing schedule for student groups...', attrs=['bold', 'underline'])
            groups = Group.objects.all()
            if groups.count() == 0:
                cprint('There is no any student group.', 'red', attrs=['bold'])
                print('Please, check that they got from lms.')
                return
            for group in groups:
                print('Parsing group {}...'.format(group.name))
                group.schedule = parse_schedule_for(group.name)
                group.save()
            print('Done!')
