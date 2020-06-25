from enum import Enum, auto
from logging import error
from time import sleep
from typing import Generator, List, Optional, Tuple
from urllib.parse import quote

from lxml import html
from lxml.html import HtmlElement
from requests import HTTPError, get
from termcolor import cprint

from main.utils.exceptions import GroupListIsEmpty
from schedule.models import Day, FullTimeSchedule, Group, Place, Schedule, Teacher


class ScheduleType(Enum):
    NONE = auto()
    TEACH = auto()
    SESSION = auto()


class ScheduleParser:
    teach_url = "https://mai.ru/education/schedule/detail.php?group={group}&week={week}"
    session_url = "https://mai.ru/education/schedule/session.php?group={group}"

    def __init__(self, schedule_type: ScheduleType, force: bool = False):
        expected_types = [ScheduleType.TEACH, ScheduleType.SESSION]
        if schedule_type not in expected_types:
            raise KeyError(
                f"Wrong ScheduleType, expected: {expected_types}, got {schedule_type}"
            )

        self.type = schedule_type
        self.force = force

        if schedule_type == ScheduleType.TEACH:
            self.schedule_type = Schedule.STUDY
            self.url = self.teach_url
        elif schedule_type == ScheduleType.SESSION:
            self.schedule_type = Schedule.SESSION
            self.url = self.session_url

    def parse(self) -> None:
        cprint("Parsing schedule for student groups...", attrs=["bold", "underline"])
        groups = Group.objects.filter(study_form=Group.FULL_TIME)

        if groups.count() == 0:
            raise GroupListIsEmpty()

        for group in groups:
            if self.__version_is_equal(group):
                continue
            print("Parsing group {}...".format(group.name))
            if self.type == ScheduleType.TEACH:
                self.__parse_teach(group)
            elif self.type == ScheduleType.SESSION:
                self.__parse_session(group)
        print("Done!")

    def __version_is_equal(self, group: Group):
        try:
            version = get_version(self.url.format(group=quote(group.name), week=1))
        except HTTPError as e:
            error(f"Cant get version of schedule at {self.url}")
            raise e

        return not self.force and group.schedule_version == version

    def __parse_teach(self, group: Group) -> None:
        for week in range(1, 19):
            try:
                self.__create_schedule_instance(group, week)
            except HTTPError as e:
                self.__handle_http_error(e, group=group.name, week=week)

    def __parse_session(self, group: Group):
        try:
            self.__create_schedule_instance(group)
        except HTTPError as e:
            self.__handle_http_error(e, group=group.name)

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

        for day_str, month, week_day, items in parse_day(body):
            day, _ = Day.objects.update_or_create(
                day=day_str, month=month, week_day=week_day, week=week
            )
            for time, item_type_resp, place_list, name, teachers in parse_items(items):
                start, end = time.split(" – ")

                res_item_type = None
                for item_type_db, item_type_human in FullTimeSchedule.ITEM_TYPES:
                    if item_type_human == item_type_resp:
                        res_item_type = item_type_db
                        break
                if not res_item_type:
                    raise KeyError(f"Item type not found for {item_type_resp}")

                item, _ = FullTimeSchedule.objects.update_or_create(
                    starts_at=start,
                    ends_at=end,
                    item_type=res_item_type,
                    name=name,
                    day=day_str,
                    schedule_type=self.schedule_type,
                    group=group,
                )

                for place in place_list:
                    building, number = normalize_place(place)
                    p, _ = Place.objects.update_or_create(
                        building=building, number=number
                    )
                    item.places.add(p.id)
                for teacher in teachers:
                    if not teacher:
                        continue
                    lastname, firstname, *_middlename = teacher.split(" ")
                    middlename = " ".join(_middlename)
                    t, _ = Teacher.objects.update_or_create(
                        lastname=lastname, firstname=firstname, middlename=middlename
                    )
                    item.teachers.add(t.id)
        sleep(1)


def get_version(url: str) -> Optional[str]:
    resp = get(url)
    if not resp.ok:
        resp.raise_for_status()

    tree = html.fromstring(resp.content)
    sleep(1)
    return tree.xpath('//*[@id="schedule-content"]/div[2]/text()')[0]


def parse_day(body: str) -> Generator[Tuple[str, str, str, HtmlElement], None, None]:
    tree = html.fromstring(body)
    for element in tree.xpath('//div[@class="sc-container"]'):
        date = element.xpath('.//div[contains(@class, "sc-day-header")]/text()')[0]
        day, month = date.split(".", maxsplit=1)
        week_day = element.xpath('.//span[@class="sc-day"]/text()')[0]
        items = element.xpath('.//div[contains(@class, "sc-table-detail")]')[0]

        yield day, month, week_day, items


def parse_items(
    element: HtmlElement,
) -> Generator[Tuple[str, str, str, str, List[str]], None, None]:
    for item in element.xpath('.//div[@class="sc-table-row"]'):
        time = item.xpath('.//div[contains(@class, "sc-item-time")]/text()')[0]
        item_type = item.xpath('.//div[contains(@class, "sc-item-type")]/text()')[0]
        place_list = item.xpath('.//div[contains(@class, "sc-item-location")]/text()')
        name = item.xpath('.//*[@class="sc-title"]/text()')[0]
        try:
            teachers = item.xpath('.//span[@class="sc-lecturer"]/text()')[0].split(", ")
        except IndexError:
            teachers = []

        yield time, item_type, place_list, name, teachers


def normalize_place(place_list: str) -> Tuple[str, Optional[str]]:
    place_list = place_list.replace("--", "")
    place = place_list.split(" ", maxsplit=1)
    try:
        return place[0], place[1]
    except IndexError:
        return place[0], None
