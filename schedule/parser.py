from dataclasses import dataclass
from typing import List

import requests
from lxml import html
from lxml.html import HtmlElement
from requests.exceptions import Timeout


@dataclass
class Item:
    time: str
    item_type: str
    name: str
    place: str
    teachers: str


@dataclass
class Table:
    day: str
    date: str
    items: List[Item]


class ScheduleParser:
    def __init__(self, group, week=None, **kwargs):
        """Constructor of ScheduleParser

        Parameters
        ----------
        group : str
            Name of study group
        week : int, optional
            Number of study week (the default is None, which means unused in request)

        """
        self.params = {"group": group}
        if week:
            self.params["week"] = week
        self.group = group
        self.__url = "https://mai.ru/education/schedule/detail.php"
        self.__result = self.__parse_tables()

    def __response(self):
        try:
            return requests.get(self.__url, self.params, timeout=5).text
        except Timeout:
            return ""

    def __parse_tables(self) -> List[Table]:
        """Parses tables of the extramural_schedule from `self.url`

        Returns
        -------
        List[Table]
            List of tables
        """
        tree = html.fromstring(self.__response())
        res = []
        for element in tree.xpath('//div[@class="sc-container"]'):
            date = element.xpath('.//div[contains(@class, "sc-day-header")]/text()')[0]
            day = element.xpath('.//span[@class="sc-day"]/text()')[0]
            items = element.xpath('.//div[contains(@class, "sc-table-detail")]')[0]
            res.append(Table(day=day, date=date, items=self.__parse_items(items)))
        return res

    @staticmethod
    def __parse_items(element: HtmlElement) -> List[Item]:
        """Parses items from given table

        Parameters
        ----------
        element : HtmlElement
            lxml

        Returns
        -------
        List[Item]
            List of parsed `Item`s
        """
        res: List[Item] = []
        for item in element.xpath('.//div[@class="sc-table-row"]'):
            time = item.xpath('.//div[contains(@class, "sc-item-time")]/text()')[0]
            item_type = item.xpath('.//div[contains(@class, "sc-item-type")]/text()')[0]
            place = item.xpath('.//div[contains(@class, "sc-item-location")]/text()')[0]
            name = item.xpath('.//*[@class="sc-title"]/text()')[0]
            try:
                teachers = item.xpath('.//span[@class="sc-lecturer"]/text()')[0]
            except IndexError:
                teachers = ""
            res.append(
                Item(
                    time=time,
                    item_type=item_type,
                    name=name,
                    place=place,
                    teachers=teachers,
                )
            )
        return res

    @property
    def result(self):
        return self.__result
