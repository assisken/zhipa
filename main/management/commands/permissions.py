from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from termcolor import cprint

from main import models


class Command(BaseCommand):
    help = "Manage applications user permissions"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--init", action="store_true", help="Creates base permissions"
        )
        parser.add_argument("--noinput", action="store_true", help="Same as --init")

    def handle(self, *args, **options):
        if options["init"] or options["noinput"]:
            self.__init()

    def __init(self):
        cprint("Creating permission groups...", attrs=["bold", "underline"])
        group, _ = Group.objects.get_or_create(name="Корреспондент")
        news = ContentType.objects.get_for_model(models.News)
        group.permissions.add(
            Permission.objects.get(codename="add_news", content_type=news),
            Permission.objects.get(codename="change_news", content_type=news),
            Permission.objects.get(codename="delete_news", content_type=news),
        )

        group, _ = Group.objects.get_or_create(name="Расписание")
        schedule = ContentType.objects.get_for_model(models.Schedule)
        group.permissions.add(
            Permission.objects.get(codename="add_schedule", content_type=schedule),
            Permission.objects.get(codename="change_schedule", content_type=schedule),
            Permission.objects.get(codename="delete_schedule", content_type=schedule),
        )

        group, _ = Group.objects.get_or_create(name="Редактор публикаций")
        publication = ContentType.objects.get_for_model(models.Publication)
        group.permissions.add(
            Permission.objects.get(
                codename="add_publication", content_type=publication
            ),
            Permission.objects.get(
                codename="change_publication", content_type=publication
            ),
            Permission.objects.get(
                codename="delete_publication", content_type=publication
            ),
        )
        print("Done successfully!")
