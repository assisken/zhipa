from django.conf import settings
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from termcolor import cprint

from main.utils.exceptions import (
    GroupListIsEmpty,
    LmsDoesNotRespondError,
    LmsRespondsAnEmptyListError,
)
from schedule.management.scripts.groups import fetch_groups, fetch_groups_from_csv
from schedule.management.scripts.schedule import ScheduleParser, ScheduleType


class Command(BaseCommand):
    help = "Manipulates with database groups"
    requires_migrations_checks = True

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--lms", action="store_true", help="Get groups from lms")
        parser.add_argument(
            "--schedule", action="store_true", help="Get schedule from mai"
        )
        parser.add_argument(
            "--session", action="store_true", help="Get session schedule from mai"
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
        force: bool = options["force"]

        if options["schedule"]:
            schedule_type = ScheduleType.TEACH
        elif options["session"]:
            schedule_type = ScheduleType.SESSION
        else:
            schedule_type = ScheduleType.NONE

        if options["lms"]:
            cprint("Adding student groups...", attrs=["bold", "underline"])
            try:
                fetch_groups(
                    settings.LMS_URL, settings.LMS_PASSWORD, settings.DEPARTMENT
                )
            except LmsDoesNotRespondError as e:
                cprint(
                    "Seems like lms does not response with 200 code.",
                    attrs=["bold", "underline"],
                )
                print(
                    "Please, update website url or check that website does respond on url:"
                )
                print(e.args[0])
            except LmsRespondsAnEmptyListError as e:
                cprint(
                    "Lms responds an empty list, null or false that does not correct.",
                    "red",
                    attrs=["bold"],
                )
                print("Please, check url and call with developers or administration.")
                print(e.args[0])
            else:
                print("Done!")
            finally:
                return

        elif options["file"]:
            cprint(
                "Adding student groups from csv file...", attrs=["bold", "underline"]
            )
            fetch_groups_from_csv(options.get("file"))
            return

        parser = ScheduleParser(schedule_type, force)
        try:
            parser.parse()
        except GroupListIsEmpty:
            cprint("There is no any student group.", "red", attrs=["bold"])
            print("Please, check that they got from lms.")
