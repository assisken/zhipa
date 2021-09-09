from django.core.management import BaseCommand, call_command
from django.core.management.base import CommandParser

from main.utils.exceptions import GroupListIsEmpty
from schedule.management.scripts.schedule import ScheduleParser, ScheduleType
from schedule.models import FullTimeSchedule


class Command(BaseCommand):
    help = "Command for work with schedule"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--pull",
            action="store",
            choices=["study", "session"],
            help="Pulls schedule from mai",
        )
        parser.add_argument(
            "--refresh",
            action="store",
            choices=["study", "session"],
            help="Refreshes the schedule",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Clears the unhidden schedule",
        )
        parser.add_argument(
            "--reveal", action="store_true", help="Reveals all schedule"
        )
        parser.add_argument(
            "--hidden", action="store_true", help="Parse schedule and save as hidden"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Disables skip for schedule parsing",
            default=False,
        )

    def handle(self, *args, **options):
        schedule_type = ScheduleType.NONE
        force: bool = options["force"]
        hidden: bool = options["hidden"]

        if options["refresh"]:
            call_command(
                "schedule",
                "--pull",
                options["refresh"],
                "--hidden",
                "--clean",
                "--reveal",
            )
            return

        if options.get("pull") == "study":
            schedule_type = ScheduleType.TEACH
        elif options.get("pull") == "session":
            schedule_type = ScheduleType.SESSION

        if options["pull"]:
            print(
                f"Parsing {'hidden' if hidden else ''} schedule for student groups..."
            )
            parser = ScheduleParser(schedule_type, force=force, hidden=hidden)
            try:
                parser.parse()
            except GroupListIsEmpty:
                print("There is no any student group.")
                print("Please, check that they got from lms.")

        if options["clean"]:
            print("Removing unhidden schedule items...")
            FullTimeSchedule.objects.filter(
                hidden=False, schedule_type=schedule_type
            ).delete()
        if options["reveal"]:
            print("Revealing schedule...")
            FullTimeSchedule.objects.filter(
                hidden=True, schedule_type=schedule_type
            ).update(hidden=False)
