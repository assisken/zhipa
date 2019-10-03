from datetime import datetime
from typing import Dict, List

from django.db import IntegrityError
from django.utils.timezone import make_aware
from pytz import timezone

from main.models import News, Staff
from smiap.settings import TIME_ZONE


def handle_data(data: List[Dict]):
    for item in data:
        name = item.get('name', None)
        try:
            if not name:
                continue
            elif name == 'news':
                insert_news(item['data'])
            elif name == 'staff':
                insert_staff(item['data'])
        except IntegrityError:
            continue


def insert_news(data: List[Dict]):
    for news in data:
        image = news['img']
        if image:
            image = image.replace('img/', 'images/')

        text = news['text']
        if text:
            text = text.replace('img/', 'images/')

        date = news['date']
        if date:
            date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        News.objects.create(
            title=news['title'],
            date=make_aware(date, timezone=timezone(TIME_ZONE)),
            url=news['url'],
            img=image,
            description=news['description'],
            text=text,
            hidden=news['hidden'],
        )


def insert_staff(data: List[Dict]):
    for staff in data:
        image = staff['img']
        if image:
            image = image.replace('img/', 'images/')

        Staff.objects.create(
            lastname=staff['lastname'],
            firstname=staff['firstname'],
            middlename=staff['patronymic'],
            img=image,
            regalia=staff['regalia'],
            description=staff['description'],
            leader=staff['leader'],
            lecturer=staff['lecturer'],
            hide=staff['hide'],
        )
