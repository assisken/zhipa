from collections import namedtuple
from datetime import datetime, timedelta
from typing import Dict, Union

Dates = namedtuple('Dates', 'au_start1 au_end sp_start sp_end au_start2')


def avoid_sunday(date):
    return date + timedelta(days=1) if date.weekday() == 6 else date


def current_week(date: datetime, now: datetime = datetime.now()):
    return now.isocalendar()[1] - date.isocalendar()[1] + 1


def get_dates(now):
    if now.month >= 9:
        autumn_start1 = avoid_sunday(datetime(year=now.year, month=9, day=1))
        spring_start = avoid_sunday(datetime(year=now.year + 1, month=2, day=9))
        autumn_start2 = avoid_sunday(datetime(year=now.year + 1, month=9, day=1))
    else:
        autumn_start1 = avoid_sunday(datetime(year=now.year - 1, month=9, day=1))
        spring_start = avoid_sunday(datetime(year=now.year, month=2, day=9))
        autumn_start2 = avoid_sunday(datetime(year=now.year, month=9, day=1))

    autumn_end = autumn_start1 + timedelta(days=7 * 17)
    spring_end = spring_start + timedelta(days=7 * 17)

    return Dates(autumn_start1, autumn_end, spring_start, spring_end, autumn_start2)


def date_block() -> Dict[str, Union[int, str]]:
    now = datetime.now()
    dates = get_dates(now)

    if dates.au_start1 <= now < dates.au_end:
        return {
            'text': 'Учёба продолжается',
            'num': current_week(dates.au_start1, now),
            'desc': 'неделя'
        }
    elif dates.au_end <= now < dates.sp_start:
        return {
            'text': 'Начало учёбы',
            'num': dates.sp_start.day,
            'desc': dates.sp_start.strftime('%B')
        }
    elif dates.sp_start <= now < dates.sp_end:
        return {
            'text': 'Учёба продолжается',
            'num': current_week(dates.sp_start, now),
            'desc': 'неделя'
        }
    elif dates.sp_end <= now < dates.au_start2:
        return {
            'text': 'Начало учёбы',
            'num': dates.au_start2.day,
            'desc': dates.au_start2.strftime('%B')
        }

    return {
        'text': '',
        'num': '404',
        'desc': 'Not Found'
    }
