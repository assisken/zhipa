import re
from typing import Any, Dict, Iterable

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from schedule.models import FullTimeSchedule, Group, Schedule, Teacher


def gen_groups_table(groups: Iterable[Group], from_week: int) -> str:
    filename = "groups"
    wb = load_workbook("template.xlsx")
    sh: Worksheet = wb["all"]

    for index, group in enumerate(groups):
        col = 2 * index + 4

        sh.cell(1, col, value=group.name)

        for week in range(17, from_week - 1, -1):
            item: FullTimeSchedule
            for item in FullTimeSchedule.objects.filter(
                group=group, day__week=week
            ).order_by("day__date"):
                day = item.day
                if not day:
                    raise ValueError(f"Item {item} has no day")

                item_type = item.item_type
                item_name = item.name
                if not item_name:
                    continue
                place = "\n".join(str(place) for place in item.places.all())
                teachers = ", ".join(str(teacher) for teacher in item.teachers.all())

                if len(item_name) > 57:
                    name_splitted = re.split(r"[ \-,.]", item_name)
                    name_uppercased = map(
                        lambda x: x[0].upper() if len(x) > 2 else x[0], name_splitted
                    )
                    item_name = "".join(name_uppercased)

                value = f"{item_name} {item_type}"
                if teachers:
                    value += f"\n{teachers}"

                fill_items(
                    sh,
                    col,
                    content=value,
                    place=place,
                    day=day.week_day,
                    time_start=item.starts_at,
                    time_end=item.ends_at,
                    week=week,
                )
    wb.save(f"{filename}.xlsx")
    return filename


def gen_teachers_table(teachers: Iterable[Teacher]) -> str:
    filename = "teachers"
    wb = load_workbook("template1.xlsx")
    sh: Worksheet = wb["all"]

    for index, teacher in enumerate(teachers):
        col = 2 * index + 4

        sh.cell(1, col, value=str(teacher))

        for week in range(17, 0, -1):
            items: Dict[str, Dict[str, Any]] = {}
            item: FullTimeSchedule
            for item in FullTimeSchedule.objects.filter(
                teachers__exact=teacher, day__week=week, schedule_type=Schedule.STUDY
            ):
                try:
                    existing = items[item.key()]
                except KeyError:
                    items[item.key()] = {
                        "day": item.day,
                        "starts_at": item.starts_at,
                        "ends_at": item.ends_at,
                        "groups": frozenset((str(item.group),)),
                        "item_type": item.item_type,
                        "name": item.name,
                        "places": frozenset(
                            (str(place) for place in item.places.all())
                        ),
                    }
                else:
                    existing["groups"] |= {str(item.group)}
                    existing["places"] |= {str(place) for place in item.places.all()}

            for _, value in items.items():
                day = value["day"]
                groups = ", ".join(sorted(value["groups"]))
                item_type = value["item_type"]
                item_name = value["name"]
                if not item_name:
                    continue
                place = "\n".join(value["places"])

                if len(item_name) > 57:
                    name_splitted = re.split(r"[ \-,.]", item_name)
                    name_uppercased = map(
                        lambda x: x[0].upper() if len(x) > 2 else x[0], name_splitted
                    )
                    item_name = "".join(name_uppercased)

                fill_items(
                    sh,
                    col,
                    content=f"{item_name} {item_type}\n{groups}",
                    place=place,
                    day=day.week_day,
                    time_start=value["starts_at"],
                    time_end=value["ends_at"],
                    week=week,
                )

    wb.save(f"{filename}.xlsx")
    return filename


def fill_items(sheet: Worksheet, col: int, **kwargs) -> None:
    content = kwargs.get("content")
    place = kwargs.get("place")
    day = kwargs.get("day")
    time_start = kwargs.get("time_start")
    time_end = kwargs.get("time_end")
    if not time_start:
        raise ValueError(f"Not found time_start at {content}")
    if not time_end:
        raise ValueError(f"Not found time_end at {content}")

    time = "{} – {}".format(time_start.strftime("%H:%M"), time_end.strftime("%H:%M"))
    week = kwargs.get("week")
    if not week:
        raise ValueError(f"Not found week at {content}")

    week_offset = abs((week - 1) % 2)

    if day == "Пн":
        day_offset = 0 * 14
    elif day == "Вт":
        day_offset = 1 * 14
    elif day == "Ср":
        day_offset = 2 * 14
    elif day == "Чт":
        day_offset = 3 * 14
    elif day == "Пт":
        day_offset = 4 * 14
    elif day == "Сб":
        day_offset = 5 * 14
    else:
        raise Exception(f"Unexpected day: {day}")

    if time == "09:00 – 10:30":
        row = 2
    elif time == "10:45 – 12:15":
        row = 4
    elif time == "13:00 – 14:30":
        row = 6
    elif time == "14:45 – 16:15":
        row = 8
    elif time == "16:30 – 18:00":
        row = 10
    elif time == "18:15 – 19:45":
        row = 12
    elif time == "20:00 – 21:30":
        row = 14
    else:
        raise Exception(f"Unexpected time: {time}")
    row += day_offset + week_offset

    sheet.cell(row=row, column=col, value=content)
    sheet.cell(row=row, column=col + 1, value=place)
