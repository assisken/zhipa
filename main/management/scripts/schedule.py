from collections import namedtuple
from time import sleep
from typing import Dict, List
from urllib.parse import quote

from lxml import html
from lxml.html import HtmlElement
from requests import get, exceptions

Day = namedtuple('Day', 'date day items')
Item = namedtuple('Item', 'time item_type name place teachers')


def parse_schedule_for(group: str) -> Dict[int, List[Day]]:
    url = 'https://mai.ru/education/schedule/detail.php?group={group}&week={week}'
    schedule = {}
    for week in range(1, 18):
        resp = get(url.format(group=quote(group), week=week))
        if resp.status_code != 200:
            print('Error. Received not 200 code.')
            schedule[week] = []
            continue

        body = resp.content.decode('utf8')
        schedule[week] = parse_table(body)
        sleep(1)
    return schedule


def parse_table(body: str) -> List[Day]:
    tree = html.fromstring(body)
    days = []
    for element in tree.xpath('//div[@class="sc-container"]'):
        date = element.xpath('.//div[contains(@class, "sc-day-header")]/text()')[0]
        day = element.xpath('.//span[@class="sc-day"]/text()')[0]
        items = element.xpath('.//div[contains(@class, "sc-table-detail")]')[0]

        days.append(Day(date=date, day=day, items=parse_items(items)))
    return days


def parse_items(element: HtmlElement) -> List[Item]:
    res: List[Item] = []
    for item in element.xpath('.//div[@class="sc-table-row"]'):
        time = item.xpath('.//div[contains(@class, "sc-item-time")]/text()')[0]
        item_type = item.xpath('.//div[contains(@class, "sc-item-type")]/text()')[0]
        place_list = item.xpath('.//div[contains(@class, "sc-item-location")]/text()')[0]
        name = item.xpath('.//*[@class="sc-title"]/text()')[0]
        try:
            teachers = item.xpath('.//span[@class="sc-lecturer"]/text()')[0].split(', ')
        except IndexError:
            teachers = []
        item = Item(time=time,
                    item_type=item_type,
                    name=name,
                    place=normalize_place(place_list),
                    teachers=teachers)
        res.append(item)
    return res


def normalize_place(place_list: str) -> Dict[str, str]:
    place_list = place_list.replace('--', '')
    place = place_list.split(' ')
    try:
        out = {'place': place[0], 'auditory': place[1]}
    except IndexError:
        out = {'place': place[0], 'auditory': ''}
    return out
