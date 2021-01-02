from collections import OrderedDict
from datetime import date

from main.utils.date import avoid_sunday, get_semester_year

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = OrderedDict(
    {
        "AUTUMN_SEMESTER_START": (
            avoid_sunday(date(year=get_semester_year(), month=9, day=1)),
            "Дата начала осеннего семестра",
            date,
        ),
        "SPRING_SEMESTER_START": (
            avoid_sunday(date(year=get_semester_year() + 1, month=2, day=9)),
            "Дата начала весеннего семестра",
            date,
        ),
        "NEW_YEAR_AUTUMN_SEMESTER_START": (
            avoid_sunday(date(year=get_semester_year() + 1, month=9, day=1)),
            "Дата начала осеннего семестра в следующем учебном году",
            date,
        ),
        "WEEKS_IN_SEMESTER": (18, "Количество недель в семестре", int),
        "MAI_DAY_CONTAINER_SELECTOR": (
            ".sc-table-day",
            "CSS-селектор; контейнер на сайте маи, означающий отдельный учебный день",
            str,
        ),
        "MAI_ITEM_CONTAINER_SELECTOR": (
            ".sc-table-detail .sc-table-row",
            "CSS-селектор; контейнер на сайте маи, содержащий одну пару в себе",
            str,
        ),
        "MAI_DATE_SELECTOR": (
            ".sc-day-header",
            "CSS-селектор; дата, в которое время проводятся занятия",
            str,
        ),
        "MAI_DAY_OF_WEEK_SELECTOR": (
            ".sc-day",
            "CSS-селектор; день недели, в которое проводятся занятия",
            str,
        ),
        "MAI_TIME_SELECTOR": (
            ".sc-item-time",
            "CSS-селектор; временной интервал, когда проходит пара",
            str,
        ),
        "MAI_TYPE_SELECTOR": (
            ".sc-item-type",
            "CSS-селектор; какой тип у пары (лекция, семинар, лабораторная работа и т.д.)",
            str,
        ),
        "MAI_TITLE_SELECTOR": (
            ".sc-title",
            "CSS-селектор; название пары или предмет, по которому проходит пара",
            str,
        ),
        "MAI_TEACHER_SELECTOR": (
            ".sc-lecturer",
            "CSS-селектор; преподаватели, ведущие предмет",
            str,
        ),
        "MAI_PLACE_XPATH_SELECTOR": (
            './/*[contains(@class, "sc-item-location")]/text()',
            "Xpath-селектор; в каком месте проходит пара",
            str,
        ),
    }
)
