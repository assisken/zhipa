#!/bin/env python

import json
import os
from collections import namedtuple

from smiap.settings import BASE_DIR

STAFF_PATH = '/home/aken/Downloads/staff.json'
NEWS_PATH = '/home/aken/Downloads/news.json'

Staff = namedtuple(
    'Staff', 'pk lastname firstname middlename img regalia description leader lecturer hide')
News = namedtuple('News', 'pk title date url img description text hidden')


def iter_staff():
    with open(STAFF_PATH, 'r') as file:
        all_staff = json.loads(file.read())
    for staff in all_staff:
        yield Staff(
            pk=staff['id'],
            lastname=staff['lastname'],
            firstname=staff['firstname'],
            middlename=staff['patronymic'],
            img=staff['img'],
            regalia=staff['regalia'],
            description=staff['description'],
            leader=staff['leader'],
            lecturer=staff['lecturer'],
            hide=staff['hide']
        )


def iter_news():
    with open(NEWS_PATH, 'r') as file:
        all_news = json.loads(file.read())
    for news in all_news:
        yield News(
            pk=news['id'],
            title=news['title'],
            date=news['date'],
            url=news['url'],
            img=news['img'],
            description=news['description'],
            text=news['text'],
            hidden=news['hidden']
        )


def gen_normal_staff(staff: Staff):
    return {
        'model': 'main.staff',
        'pk': staff.pk,
        'fields': {
            'lastname': staff.lastname,
            'firstname': staff.firstname,
            'middlename': staff.middlename,
            'img': staff.img,
            'regalia': staff.regalia,
            'description': staff.description,
            'leader': staff.leader,
            'lecturer': staff.lecturer,
            'hide': staff.hide
        }
    }


def gen_normal_news(news: News):
    return {
        'model': 'main.news',
        'pk': news.pk,
        'fields': {
            'title': news.title,
            'date': news.date,
            'url': news.url,
            'img': news.img,
            'description': news.description,
            'text': news.text,
            'hidden': news.hidden
        }
    }


def write_to_file(data):
    with open(os.path.join(BASE_DIR, 'news.json'), 'w') as file:
        file.write(json.dumps(data, sort_keys=True, indent=4))
