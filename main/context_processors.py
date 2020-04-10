from smiap.settings import BRAND
from main.utils.date import TeachTime, TeachState


def app_processor(request):
    nav_items = {
        'home': {"id": "home", "title": "Главная", "link": "/", "subitems": []},
        'about': {"id": "about", "title": "О кафедре", "link": "/about/intro", "subitems": [
            {"id": "intro", "title": "Введение", "link": "/about/intro"},
            {"id": "history", "title": "История кафедры", "link": "/about/history"},
            {"id": "staff", "title": "Сотрудники кафедры", "link": "/about/staff"},
            {"id": "conferences", "title": "Участие в конференциях", "link": "/about/conferences"},
            {"id": "contacts", "title": "Контакты", "link": "/about/contacts"}
        ]},

        'materials': {"id": "materials", "title": "Материалы", "link": "/materials/news", "subitems": [
            {"id": "news", "title": "Новости", "link": "/materials/news"},
            {"id": "publications", "title": "Публикации", "link": "/materials/publications"},
            {"id": "tutorials", "title": "Учебные пособия", "link": "/materials/tutorials"},
            # {"id": "session", "title": "Расписание сессии заочной формы", "link": "/materials/session"}
        ]},

        'abiturients': {"id": "abiturients", "title": "Абитуриентам", "link": "/abiturients/info", "subitems": [
            {"id": "info", "title": "Информация для абитуриентов", "link": "/abiturients/info"},
            {"id": "programs", "title": "Программа обучения", "link": "/abiturients/programs"}
        ]},

        'students': {"id": "students", "title": "Студентам", "link": "/students/timetable", "subitems": [
            {"id": "timetable", "title": "Расписания очных занятий", "link": "/students/timetable"},
            {"id": "extramural", "title": "Расписания заочных занятий", "link": "/students/timetable/extramural"}
        ]}
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

    teach_time = TeachTime()
    teach_state = teach_time.teach_state

    if teach_state == TeachState.HOLIDAYS or teach_time.week >= 17:
        nav_items['students']['subitems'].append(
            {"id": "session", "title": "Расписания очной сессии", "link": "/students/session"},
        )
        nav_items['students']['subitems'].append(
            {"id": "ex-session", "title": "Расписания заочной сессии", "link": "/students/timetable/ex-session"}
        )

    if request.path == '/':
        active_items = 'home'
    else:
        active_items = request.path.split('/')

    return {
        'APP_TITLE': BRAND,
        'NAV_ITEMS': nav_items,
        'ACTIVE_ITEMS': active_items
    }
