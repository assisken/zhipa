from django.core.management import BaseCommand, call_command

from termcolor import cprint


class Command(BaseCommand):
    help = 'Initializes the application.'

    def handle(self, *args, **options):
        cprint('Applying migrations...', attrs=['bold', 'underline'])
        call_command('migrate')
        call_command('permissions', '--init')
        call_command('import')
        call_command('groups', '--lms')
        call_command('groups', '--file', 'groups.csv')
        call_command('groups', '--extramural_schedule')
