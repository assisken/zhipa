from django.contrib.sites.models import Site

from smiap.settings.components.app import BRAND


def app_processor(request):
    kwargs = request.resolver_match.kwargs
    nav_items = {
        "home": {"id": "home", "title": "Главная", "link": "/", "subitems": []},
        "about": {
            "id": "about",
            "title": "О кафедре",
            "link": "/about/intro",
            "subitems": [
                {"id": "intro", "title": "Введение", "link": "/about/intro"},
                {"id": "history", "title": "История кафедры", "link": "/about/history"},
                {"id": "staff", "title": "Сотрудники кафедры", "link": "/about/staff"},
                {
                    "id": "conferences",
                    "title": "Участие в конференциях",
                    "link": "/about/conferences",
                },
                {"id": "contacts", "title": "Контакты", "link": "/about/contacts"},
            ],
        },
        "materials": {
            "id": "materials",
            "title": "Материалы",
            "link": "/materials/publications",
            "subitems": [
                {
                    "id": "publications",
                    "title": "Публикации",
                    "link": "/materials/publications",
                },
                {
                    "id": "tutorials",
                    "title": "Учебные пособия",
                    "link": "/materials/tutorials",
                },
            ],
        },
        "news": {
            "id": "news",
            "title": "Новости",
            "link": "/news",
            "subitems": [],
        },
        "abiturients": {
            "id": "abiturients",
            "title": "Абитуриентам",
            "link": "/abiturients/info",
            "subitems": [
                {
                    "id": "info",
                    "title": "Информация для абитуриентов",
                    "link": "/abiturients/info",
                },
                {
                    "id": "programs",
                    "title": "Программа обучения",
                    "link": "/abiturients/programs",
                },
            ],
        },
        "students": {
            "id": "students",
            "title": "Студентам",
            "link": "/students/timetable",
            "subitems": [],
        },
        "profile": {
            "id": "profile",
            "hidden": True,
            "subitems": [
                {
                    "id": "description",
                    "title": "Описание",
                    "link": "/profile/{profile}/description",
                },
                {
                    "id": "publications",
                    "title": "Публикации",
                    "link": "/profile/{profile}/publications",
                },
            ],
        },
    }

    # TODO
    # if request.user and request.user.is_authenticated:
    #     last_item = {"id": "username", "title": request.user.username, "link": None, "subitems": [
    #         {"id": "logout", "title": "Выйти", "link": "/auth/logout?next={}".format(request.path), "subitems": []}
    #     ]}
    # else:
    #     last_item = {"id": "login", "title": "Войти",
    #                  "link": "/auth/login?next={}".format(request.path), "subitems": []}
    # nav_items.append(last_item)

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
