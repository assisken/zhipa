from django.conf import settings
from django.core.management import BaseCommand
from django.core.management.base import CommandParser

from main.utils.exceptions import LmsDoesNotRespondError, LmsRespondsAnEmptyListError
from schedule.management.scripts.groups import fetch_groups, fetch_groups_from_csv
from schedule.models import Group


class Command(BaseCommand):
    help = "Manipulates with database groups"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--pull", action="store_true", help="Pull groups from lms")
        parser.add_argument(
            "--clear", action="store_true", help="Removes all groups from database"
        )
        parser.add_argument(
            "--file", action="store", help="Specify file name. Default is `groups.csv`"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Disables skip for schedule parsing",
            default=False,
        )

    def handle(self, *args, **options):
        if options["clear"]:
            print("Clearing student groups...")
            Group.objects.all().delete()

        if options["pull"]:
            print("Adding student groups...")
            try:
                fetch_groups(
                    settings.LMS_URL, settings.LMS_PASSWORD, settings.DEPARTMENT
                )
            except LmsDoesNotRespondError as e:
                print("Seems like lms does not response with 200 code.")
                print(
                    "Please, update website url or check that website does respond on url:"
                )
                print(e.args[0])
            except LmsRespondsAnEmptyListError as e:
                print(
                    "Lms responds an empty list, null or false that does not correct."
                )
                print("Please, check url and call with developers or administration.")
                print(e.args[0])
            else:
                print("Done!")

        elif options["file"]:
            print("Adding student groups from csv file...")
            fetch_groups_from_csv(options.get("file"))
            return
