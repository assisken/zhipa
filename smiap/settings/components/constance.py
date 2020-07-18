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
    }
)
