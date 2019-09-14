from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand, call_command

from termcolor import cprint

from main.models import News


class Command(BaseCommand):
    help = 'Initializes the application.'

    def handle(self, *args, **options):
        cprint('Applying migrations...', attrs=['bold', 'underline'])
        call_command('migrate')

        cprint('Creating permission groups...', attrs=['bold', 'underline'])
        group, _ = Group.objects.get_or_create(name='Корреспондент')
        news = ContentType.objects.get_for_model(News)
        group.permissions.add(
            Permission.objects.get(codename='add_news', content_type=news),
            Permission.objects.get(codename='change_news', content_type=news),
            Permission.objects.get(codename='delete_news', content_type=news),
        )
        print('Done successfully!')

        call_command('import')
        call_command('groups', '--lms')
        call_command('groups', '--file', 'groups.csv')
        call_command('groups', '--schedule')
