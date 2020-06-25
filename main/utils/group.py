import re

from main.types import Degree


def degree(group_name: str) -> Degree:
    match = re.search(r"-\S+(Б|Бк|М|Мк|А)-", group_name)
    if not match:
        raise ValueError(f"No degree in group {group_name}")

    res = match.group(1)
    if res == "Б" or res == "Бк":
        return Degree.BACHELOR
    elif res == "М" or res == "Мк":
        return Degree.MASTER
    elif res == "А":
        return Degree.GRADUATE
    else:
        raise ValueError("Group does not match")


def study_form(group_name: str) -> str:
    match = re.search(r"^\S+([ОЗ])-", group_name)
    if not match:
        raise ValueError(f"Study form not found at group {group_name}")

    res = match.group(1)
    if res == "О":
        return "очная"
    elif res == "З":
        return "заочная"
    raise ValueError("Got not provided study form")
