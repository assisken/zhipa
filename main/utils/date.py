import re
from datetime import date, timedelta
from enum import Enum, Flag, auto
from typing import Optional

from constance import config

MONTH_GENITIVE = {
    1: "Января",
    2: "Февраля",
    3: "Марта",
    4: "Апреля",
    5: "Мая",
    6: "Июня",
    7: "Июля",
    8: "Августа",
    9: "Сентября",
    10: "Октября",
    11: "Ноября",
    12: "Декабря",
}


def get_week(d: date) -> int:
    return d.isocalendar()[1]


def get_semester_year(now=date.today()) -> int:
    month_start = 9
    if now.month >= month_start:
        return now.year
    else:
        return now.year - 1


def avoid_sunday(current_date: date) -> date:
    if current_date.weekday() == 6:
        current_date += timedelta(days=1)
    return current_date


def date_block(teach_time: "TeachTime"):
    teach_state = teach_time.teach_state
    if teach_state.it_is(TeachState.SEMESTER):
        return {"text": "Учёба продолжается", "num": teach_time.week, "desc": "неделя"}
    elif teach_state.it_is(TeachState.HOLIDAYS):
        return {
            "text": "Начало учёбы",
            "num": teach_time.next_start.day,
            "desc": MONTH_GENITIVE[teach_time.next_start.month],
        }

    return {"text": "", "num": "404", "desc": "Not Found"}


class TeachState(Flag):
    AUTUMN_SEMESTER = auto()
    WINTER_HOLIDAYS = auto()
    SPRING_SEMESTER = auto()
    SUMMER_HOLIDAYS = auto()

    SEMESTER = AUTUMN_SEMESTER | SPRING_SEMESTER
    HOLIDAYS = WINTER_HOLIDAYS | SUMMER_HOLIDAYS

    AUTUMN = AUTUMN_SEMESTER | WINTER_HOLIDAYS
    SPRING = SPRING_SEMESTER | SUMMER_HOLIDAYS

    def it_is(self, comp: Enum):
        return self.value & comp.value > 0


# TODO: Check if bug in django-constance
def _to_date(_date) -> date:
    if isinstance(_date, date):
        return _date
    elif isinstance(_date, str):
        return date.fromisoformat(_date)
    raise ValueError(f"Type {type(_date)} for date ({date!r}) is not supported")


class TeachTime:
    month_start = 9

    def __init__(self, now=date.today()):
        self.now = now
        self.weeks_in_semester: int = config.WEEKS_IN_SEMESTER
        self.__autumn_start1: date = _to_date(config.AUTUMN_SEMESTER_START)
        self.__spring_start: date = _to_date(config.SPRING_SEMESTER_START)
        self.__autumn_start2: date = _to_date(config.NEW_YEAR_AUTUMN_SEMESTER_START)
        self.__autumn_end = self.__autumn_start1 + timedelta(
            days=7 * self.weeks_in_semester
        )
        self.__spring_end = self.__spring_start + timedelta(
            days=7 * self.weeks_in_semester
        )

        self.teach_state = self.__teach_time(now)

    @property
    def start(self) -> date:
        if self.teach_state.it_is(TeachState.AUTUMN):
            return self.__autumn_start1
        elif self.teach_state.it_is(TeachState.SPRING):
            return self.__spring_start
        raise ValueError(
            f"Can't get current start with teach_time = {self.teach_state}"
        )

    @property
    def end(self) -> date:
        if self.teach_state.it_is(TeachState.AUTUMN):
            return self.__autumn_end
        elif self.teach_state.it_is(TeachState.SPRING):
            return self.__spring_end
        raise ValueError(f"Can't get current end with teach_time = {self.teach_state}")

    @property
    def next_start(self) -> date:
        if self.teach_state.it_is(TeachState.AUTUMN):
            return self.__spring_start
        elif self.teach_state.it_is(TeachState.SPRING):
            return self.__autumn_start2
        raise ValueError("Got not provided teach state")

    @property
    def week(self) -> int:
        current_week = get_week(self.now)
        start_week = get_week(self.start)
        if current_week >= start_week:
            return current_week - start_week + 1
        else:
            last_week = get_week(self.now - timedelta(weeks=current_week))
            weeks_last_year = last_week - start_week
            return weeks_last_year + current_week + 1

    def __teach_time(self, now: date) -> TeachState:
        if self.__autumn_start1 <= now < self.__autumn_end:
            return TeachState.AUTUMN_SEMESTER
        elif self.__autumn_end <= now < self.__spring_start:
            return TeachState.WINTER_HOLIDAYS
        elif self.__spring_start <= now < self.__spring_end:
            return TeachState.SPRING_SEMESTER
        elif self.__spring_end <= now < self.__autumn_start2:
            return TeachState.SUMMER_HOLIDAYS
        else:
            return TeachState.AUTUMN_SEMESTER


def get_year_from_string(string: str) -> Optional[str]:
    found = re.search(r"\b((19|20)\d{2})", string)
    return None if found is None else found.group(0)
