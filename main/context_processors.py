from typing import Dict, List, Optional, TypedDict

from django.contrib.sites.models import Site

from main.utils.date import TeachState, TeachTime
from smiap.settings.components.app import BRAND


class NavigationSubItem(TypedDict):
    id: str
    title: str
    hidden: bool
    link: Optional[str]


class NavigationItem(NavigationSubItem):
    subitems: List[NavigationSubItem]


NavigationItems = Dict[str, NavigationItem]


def app_processor(request):
    kwargs = request.resolver_match.kwargs
    nav_items: NavigationItems = {
        "home": {
            "id": "home",
            "title": "Главная",
            "hidden": False,
            "link": "/",
            "subitems": [],
        },
        "about": {
            "id": "about",
            "title": "О кафедре",
            "hidden": False,
            "link": "/about/intro",
            "subitems": [
                {
                    "id": "intro",
                    "title": "Введение",
                    "hidden": False,
                    "link": "/about/intro",
                },
                {
                    "id": "history",
                    "title": "История кафедры",
                    "hidden": False,
                    "link": "/about/history",
                },
                {
                    "id": "staff",
                    "title": "Сотрудники кафедры",
                    "hidden": False,
                    "link": "/about/staff",
                },
                {
                    "id": "conferences",
                    "title": "Участие в конференциях",
                    "hidden": False,
                    "link": "/about/conferences",
                },
                {
                    "id": "contacts",
                    "title": "Контакты",
                    "hidden": False,
                    "link": "/about/contacts",
                },
            ],
        },
        "materials": {
            "id": "materials",
            "title": "Материалы",
            "hidden": False,
            "link": "/materials/news",
            "subitems": [
                {
                    "id": "news",
                    "title": "Новости",
                    "hidden": False,
                    "link": "/materials/news",
                },
                {
                    "id": "publications",
                    "title": "Публикации",
                    "hidden": False,
                    "link": "/materials/publications",
                },
                {
                    "id": "tutorials",
                    "title": "Учебные пособия",
                    "hidden": False,
                    "link": "/materials/tutorials",
                },
                # {"id": "session", "title": "Расписание сессии заочной формы", "link": "/materials/session"}
            ],
        },
        "abiturients": {
            "id": "abiturients",
            "title": "Абитуриентам",
            "hidden": False,
            "link": "/abiturients/info",
            "subitems": [
                {
                    "id": "info",
                    "title": "Информация для абитуриентов",
                    "hidden": False,
                    "link": "/abiturients/info",
                },
                {
                    "id": "programs",
                    "title": "Программа обучения",
                    "hidden": False,
                    "link": "/abiturients/programs",
                },
            ],
        },
        "students": {
            "id": "students",
            "title": "Студентам",
            "hidden": False,
            "link": "/students/timetable",
            "subitems": [
                {
                    "id": "timetable",
                    "title": "Расписания очных занятий",
                    "hidden": False,
                    "link": "/students/timetable",
                },
                {
                    "id": "extramural",
                    "title": "Расписания заочных занятий",
                    "hidden": False,
                    "link": "/students/timetable/extramural",
                },
            ],
        },
        "profile": {
            "id": "profile",
            "title": "Профиль",
            "hidden": True,
            "link": "",
            "subitems": [
                {
                    "id": "description",
                    "title": "Описание",
                    "hidden": False,
                    "link": "/profile/{profile}/description",
                },
                {
                    "id": "publications",
                    "title": "Публикации",
                    "hidden": False,
                    "link": "/profile/{profile}/publications",
                },
            ],
        },
    }

    last_item: NavigationItem
    if request.user and request.user.is_authenticated:
        last_item = {
            "id": "accounts",
            "title": request.user.username,
            "hidden": False,
            "link": "/accounts/info",
            "subitems": [
                {
                    "id": "info",
                    "title": "Мой аккаунт",
                    "hidden": False,
                    "link": "/accounts/info",
                },
                {
                    "id": "profile",
                    "title": "Мой профиль",
                    "hidden": False,
                    "link": "/accounts/profile",
                },
                {
                    "id": "logout",
                    "title": "Выйти",
                    "hidden": False,
                    "link": "/accounts/logout?next={}".format(request.path),
                },
            ],
        }
    else:
        last_item = {
            "id": "login",
            "title": "Войти",
            "hidden": False,
            "link": "/accounts/login?next={}".format(request.path),
            "subitems": [
                {
                    "id": "registration",
                    "title": "Регистрация",
                    "hidden": False,
                    "link": "/accounts/register/",
                }
            ],
        }
    nav_items["login"] = last_item

    teach_time = TeachTime()
    teach_state = teach_time.teach_state

    if teach_state == TeachState.HOLIDAYS or teach_time.week >= 17:
        nav_items["students"]["subitems"].append(
            {
                "id": "session",
                "title": "Расписания очной сессии",
                "link": "/students/session",
            },
        )
        nav_items["students"]["subitems"].append(
            {
                "id": "ex-session",
                "title": "Расписания заочной сессии",
                "link": "/students/timetable/ex-session",
            }
        )

    if request.path == "/":
        active_items = "home"
    else:
        active_items = request.path.split("/")

    profile = kwargs.get("profile")
    if profile:
        for nav_item in nav_items["profile"]["subitems"]:
            nav_item["link"] = nav_item["link"].format(profile=profile)

    return {
        "ACTIVE_ITEMS": active_items,
        "APP_TITLE": BRAND,
        "NAV_ITEMS": nav_items,
        "SCHEME": request.scheme,
        "DOMAIN": Site.objects.get_current().domain,
    }
