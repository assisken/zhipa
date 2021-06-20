from enum import Enum
from typing import Iterable, List, Type, TypedDict, Union

from schedule.models import Schedule


class WeekDay(str, Enum):
    MONDAY = "Пн"
    TUESDAY = "Вт"
    WEDNESDAY = "Ср"
    THURSDAY = "Чт"
    FRIDAY = "Пт"
    SATURDAY = "Сб"
    EMPTY = ""


class Week(int, Enum):
    FIRST = 1
    SECOND = 2


class ScheduleRow(TypedDict):
    week: Week
    week_day: WeekDay
    date: str
    time: str
    group_name: str
    title: str
    lesson_type: str
    place: str
    teachers: List[str]


def week_from_week_number(week_number: int) -> Week:
    return Week(week_number % 2)


def week_day_from_string(week_day) -> WeekDay:
    return WeekDay(week_day[:2])


def get_schedule_table(
    schedule_model: Type[Schedule], group_study_form: str
) -> List[ScheduleRow]:
    schedule = schedule_model.objects.prefetch_related("group", "teachers").filter(
        group__study_form=group_study_form
    )

    return [
        ScheduleRow(
            week=week_from_week_number(s.week),
            week_day=week_day_from_string(s.week_day),
            date=s.date,
            time=s.time,
            group_name=s.group.name,
            title=s.name,
            lesson_type=s.item_type,
            teachers=[str(t) for t in s.teachers.all()],
            place=s.place,
        )
        for s in schedule
    ]
