from dataclasses import dataclass
from enum import Enum, auto
from functools import partial
from logging import error
from operator import attrgetter
from time import sleep
from typing import Callable, List, Optional, Tuple
from urllib.parse import quote

from constance import config
from funcy import compose, first, lkeep, lmap, notnone, select
from lxml import html
from lxml.html import HtmlElement
from progress.bar import IncrementalBar
from requests import HTTPError, get

from main.utils.exceptions import GroupListIsEmpty
from schedule.models import FullTimeSchedule, Group, Schedule, Teacher


@dataclass(frozen=True)
class Item:
    date: str
    week_day: str
    time: str
    type: str
    title: str
    place: str
    teachers: List[str]


class ScheduleType(str, Enum):
    NONE = auto()
    TEACH = Schedule.STUDY
    SESSION = Schedule.SESSION


class ScheduleParser:
    teach_url = "https://mai.ru/education/schedule/detail.php?group={group}&week={week}"
    session_url = "https://mai.ru/education/schedule/session.php?group={group}"

    def __init__(
        self, schedule_type: ScheduleType, force: bool = False, hidden: bool = False
    ):
        expected_types = [ScheduleType.TEACH, ScheduleType.SESSION]
        if schedule_type not in expected_types:
            raise KeyError(
                f"Wrong ScheduleType, expected: {expected_types}, got {schedule_type}"
            )

        self.type = schedule_type
        self.force = force
        self.hidden = hidden

        if schedule_type == ScheduleType.TEACH:
            self.schedule_type = Schedule.STUDY
            self.url = self.teach_url
        elif schedule_type == ScheduleType.SESSION:
            self.schedule_type = Schedule.SESSION
            self.url = self.session_url

    def parse(self) -> None:
        groups = Group.objects.filter(study_form=Group.FULL_TIME)

        if groups.count() == 0:
            raise GroupListIsEmpty()

        for group in groups:
            if self.type == ScheduleType.TEACH:
                self.__parse_teach(group)
            elif self.type == ScheduleType.SESSION:
                self.__parse_session(group)

    def __parse_teach(self, group: Group) -> None:
        with IncrementalBar(
            f"{group.name} ",
            max=config.WEEKS_IN_SEMESTER + 1,
            suffix="%(index)d/%(max)d week, %(elapsed)ds",
        ) as bar:
            bar.next()  # Start progress bar with 1st week
            for week in range(1, config.WEEKS_IN_SEMESTER + 1):
                try:
                    self.__create_schedule_instance(group, week)
                except HTTPError as e:
                    self.__handle_http_error(e, group=group.name, week=week)
                bar.next()

            item_count = FullTimeSchedule.objects.filter(
                group=group, hidden=True, schedule_type=Schedule.STUDY
            ).count()
            bar.write(f"Parsed {item_count} items!")

    def __parse_session(self, group: Group):
        print(f"Parsing group {group.name}...")
        try:
            self.__create_schedule_instance(group)
        except HTTPError as e:
            self.__handle_http_error(e, group=group.name)
        item_count = FullTimeSchedule.objects.filter(
            group=group, hidden=True, schedule_type=Schedule.SESSION
        ).count()
        print(f"Parsed {item_count} items!")

    @staticmethod
    def __handle_http_error(e: HTTPError, **context):
        group_name = context["group"]
        week = context["week"]
        error(f"Caught {e.response.code} at group {group_name} and week {week}")

    def __create_schedule_instance(self, group: Group, week: Optional[int] = None):
        resp = get(self.url.format(group=quote(group.name), week=week))
        if not resp.ok:
            resp.raise_for_status()
        body = resp.content.decode("utf8")

        for item in parse_schedule(body):
            schedule, _ = FullTimeSchedule.objects.update_or_create(
                date=item.date,
                week_day=item.week_day,
                week=week,
                time=item.time,
                item_type=item.type,
                name=item.title,
                place=item.place,
                schedule_type=self.schedule_type,
                group=group,
                hidden=self.hidden,
            )

            for teacher in item.teachers:
                if not teacher:
                    continue
                lastname, firstname, *_middlename = teacher.split(" ")
                middlename = " ".join(_middlename)
                t, _ = Teacher.objects.update_or_create(
                    lastname=lastname, firstname=firstname, middlename=middlename
                )
                schedule.teachers.add(t.id)
        sleep(1)


def parse_schedule(body: str) -> Tuple[Item, ...]:
    def selector(css_class: str) -> Callable:
        return compose(
            partial(lmap, str.strip),
            partial(select, notnone),
            partial(lmap, attrgetter("text")),
            partial(HtmlElement.cssselect, expr=css_class),
        )

    tree: HtmlElement = html.fromstring(body)
    select_day_containers = partial(
        HtmlElement.cssselect, expr=config.MAI_DAY_CONTAINER_SELECTOR
    )
    select_item_containers = partial(
        HtmlElement.cssselect, expr=config.MAI_ITEM_CONTAINER_SELECTOR
    )
    select_dates = selector(config.MAI_DATE_SELECTOR)
    select_days_of_week = selector(config.MAI_DAY_OF_WEEK_SELECTOR)
    select_times = selector(config.MAI_TIME_SELECTOR)
    select_types = selector(config.MAI_TYPE_SELECTOR)
    select_titles = selector(config.MAI_TITLE_SELECTOR)
    select_teachers = selector(config.MAI_TEACHER_SELECTOR)
    select_places = compose(
        lkeep,
        partial(lmap, str.strip),
        partial(select, notnone),
        partial(HtmlElement.xpath, _path=config.MAI_PLACE_XPATH_SELECTOR),
    )
    return tuple(
        Item(
            date=first(select_dates(day_container)) or "",
            week_day=first(select_days_of_week(day_container)) or "",
            time=first(select_times(item_container)) or "",
            type=first(select_types(item_container)) or "",
            title=first(select_titles(item_container)) or "",
            place=first(select_places(item_container)) or "",
            teachers=select_teachers(item_container),
        )
        for day_container in select_day_containers(tree)
        for item_container in select_item_containers(day_container)
    )
