from time import sleep
from typing import List, Tuple, Optional, Generator
from urllib.parse import quote

from lxml import html
from lxml.html import HtmlElement
from requests import get

from main.models import Day, Item, Teacher, Group, Place


def create_schedule_for(group_name: str, force: bool):
    url = 'https://mai.ru/education/schedule/detail.php?group={group}&week={week}'

    group = Group.objects.get(name=group_name)
    version = get_version(url.format(group=quote(group_name), week=1))
    if not force and group.schedule_version == version:
        return

    group.schedule_version = version
    group.save()

    for week in range(1, 19):
        resp = get(url.format(group=quote(group_name), week=week))
        if resp.status_code != 200:
            print('Error. Received not 200 code.')
            continue

        body = resp.content.decode('utf8')

        for date, day, items in parse_day(body):
            day, _ = Day.objects.get_or_create(date=date, day=day, week=week)

            for time, item_type, place_list, name, teachers in parse_items(items):
                start, end = time.split(' – ')
                item, _ = Item.objects.get_or_create(starts_at=start, ends_at=end, type=item_type,
                                                     name=name, day=day)
                item.groups.add(group.id)

                for place in place_list:
                    building, number = normalize_place(place)
                    p, _ = Place.objects.get_or_create(building=building, number=number)
                    item.places.add(p.id)
                for teacher in teachers:
                    if not teacher:
                        continue
                    lastname, firstname, middlename = teacher.split(' ')
                    t, _ = Teacher.objects.get_or_create(lastname=lastname, firstname=firstname, middlename=middlename)
                    item.teachers.add(t.id)
        sleep(1)


def get_version(url: str) -> Optional[str]:
    resp = get(url)

    if resp.status_code != 200:
        print('Error. Received not 200 code.')
        return None

    tree = html.fromstring(resp.content)
    sleep(1)
    return tree.xpath('//*[@id="schedule-content"]/div[2]/text()')[0]


def parse_day(body: str) -> Generator[Tuple[str, str, HtmlElement], None, None]:
    tree = html.fromstring(body)
    for element in tree.xpath('//div[@class="sc-container"]'):
        date = element.xpath('.//div[contains(@class, "sc-day-header")]/text()')[0]
        day = element.xpath('.//span[@class="sc-day"]/text()')[0]
        items = element.xpath('.//div[contains(@class, "sc-table-detail")]')[0]

        yield date, day, items


def parse_items(element: HtmlElement) -> Generator[Tuple[str, str, str, str, List[str]], None, None]:
    for item in element.xpath('.//div[@class="sc-table-row"]'):
        time = item.xpath('.//div[contains(@class, "sc-item-time")]/text()')[0]
        item_type = item.xpath('.//div[contains(@class, "sc-item-type")]/text()')[0]
        place_list = item.xpath('.//div[contains(@class, "sc-item-location")]/text()')
        name = item.xpath('.//*[@class="sc-title"]/text()')[0]
        try:
            teachers = item.xpath('.//span[@class="sc-lecturer"]/text()')[0].split(', ')
        except IndexError:
            teachers = []

        yield time, item_type, place_list, name, teachers


def normalize_place(place_list: str) -> Tuple[str, Optional[str]]:
    place_list = place_list.replace('--', '')
    place = place_list.split(' ', maxsplit=1)
    try:
        return place[0], place[1]
    except IndexError:
        return place[0], None
