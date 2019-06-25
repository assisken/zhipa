import re

from main.types import Degree


def degree(group_name: str) -> Degree:
    match = re.search(r'-\S+(Б|Бк|М|Мк|А)-', group_name)
    res = match.group(1)
    if res == 'Б' or res == 'Бк':
        return Degree.BACHELOR
    elif res == 'М' or res == 'Мк':
        return Degree.MASTER
    elif res == 'А':
        return Degree.GRADUATE
    else:
        raise ValueError('Group does not match')
