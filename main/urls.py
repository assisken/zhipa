from django.urls import path, register_converter, include
from django.views.generic import TemplateView

from . import converters
from .views import *

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitConverter, 'mm')
register_converter(converters.TwoDigitConverter, 'dd')

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('abiturients', TemplateView.as_view(
        template_name='abiturients/index.html'), name='abiturients'),
    path('conferences', TemplateView.as_view(
        template_name='conferences/index.html'), name='programs'),
    path('programs', TemplateView.as_view(
        template_name='programs/index.html'), name='programs'),

    path('about', TemplateView.as_view(
        template_name='about/intro.html'), name='about'),
    path('about/intro',
         TemplateView.as_view(template_name='about/intro.html'), name='intro'),
    path('about/history', HistoryView.as_view(), name='history'),
    path('about/history/page<int:number>',
         HistoryView.as_view(), name='history'),
    path('about/staff', StaffView.as_view(), name='staff'),
    path('about/contacts',
         TemplateView.as_view(template_name='about/contacts.html'), name='contacts'),

    path('materials/', NewsListView.as_view()),
    path('materials/tutorials',
         TemplateView.as_view(template_name='materials/tutorials.html'), name='tutorials'),
    path('materials/timetable', TimetableView.as_view(), name='timetable'),
    path('materials/publications',
         TemplateView.as_view(template_name='materials/publications.html'), name='publications'),
    path('materials/timetable/extramural',
         TemplateView.as_view(template_name='layout/base.html'), name='timetable-extramural'),

    path('materials/news', NewsListView.as_view(), name='news-list-begin'),
    path('materials/news/page<int:number>',
         NewsListView.as_view(), name='news-list'),
    path('materials/news/id/<int:pk>', NewsDetailView.as_view(), name='news'),
    path('materials/<yyyy:year>', NewsDateListView.as_view(), name='news-date'),
    path('materials/<yyyy:year>/<mm:month>',
         NewsDateListView.as_view(), name='news-date'),
    path('materials/<yyyy:year>/<mm:month>/<dd:day>',
         NewsDateListView.as_view(), name='news-date'),
    path('materials/news/<yyyy:year>/<mm:month>/<dd:day>/<slug:url>',
         NewsDateDetailView.as_view(), name='news-date-url'),

    path('auth/login', SmiapLoginView.as_view(), name='login'),
]

#  "/about",
#  "/about/intro",
#  "/about/history",
#  "/about/staff",
#  "/about/contacts",
#  "/materials",
#  "/materials/news",
#  "/materials/publications",
#  "/materials/tutorials",
#  "/materials/timetable",
#  "/materials/timetable/extramural",
#  "/programs",
#  "/conferences",
#  "/abiturients",
#  "/materials/news/id/35",
#  "/materials/news/2018/11/28/spacehackathon",
#  "/materials/news/2018/11/26/aviahackathon",
#  "/about/history/page2",
#  "/about/history/page3",
#  "/about/history/page4",
#  "/materials/news/2018/09/25/unisreda",
#  "/materials/news/2018/09/11/linux",
#  "/materials/news/page1",
#  "/materials/news/page2",
#  "/materials/news/page3",
#  "/materials/news/page4",
#  "/materials/news/page5",
#  "/materials/news/2018",
#  "/materials/news/2018/12",
#  "/materials/news/2018/12/05",
#  "/materials/news/2018/11",
#  "/materials/news/2018/11/28",
#  "/materials/news/2018/11/26",
#  "/materials/news/2018/09",
#  "/materials/news/2018/09/25",
#  "/materials/news/2018/09/11",
#  "/materials/news/id/29",
#  "/materials/news/id/28",
#  "/materials/news/2017/04/25/educon2017",
#  "/materials/news/2017/04/12/gagarinconf",
#  "/materials/news/id/25",
#  "/materials/news/id/23",
#  "/materials/news/id/24",
#  "/materials/news/id/22",
#  "/materials/news/id/21",
#  "/materials/news/id/20",
#  "/materials/news/id/19",
#  "/materials/news/id/18",
#  "/materials/news/id/17",
#  "/materials/news/2015/05/15/Open-Day-Rzhev",
#  "/materials/news/id/11",
#  "/materials/news/id/12",
#  "/materials/news/id/4",
#  "/materials/news/id/2",
#  "/materials/news/id/1",
#  "/materials/news/id/0",
#  "/materials/news/2018/page1",
#  "/materials/news/2018/page2",
#  "/materials/news/2018/09/06",
#  "/materials/news/2017",
#  "/materials/news/2017/09",
#  "/materials/news/2017/09/04",
#  "/materials/news/2017/04",
#  "/materials/news/2017/04/25",
#  "/materials/news/2017/04/12",
#  "/materials/news/2017/04/10",
#  "/materials/news/2016",
#  "/materials/news/2016/12",
#  "/materials/news/2016/12/17",
#  "/materials/news/2016/09",
#  "/materials/news/2016/09/21",
#  "/materials/news/2016/06",
#  "/materials/news/2016/06/18",
#  "/materials/news/2016/04",
#  "/materials/news/2016/04/14",
#  "/materials/news/2016/04/13",
#  "/materials/news/2016/01",
#  "/materials/news/2016/01/29",
#  "/materials/news/2015",
#  "/materials/news/2015/11",
#  "/materials/news/2015/11/21",
#  "/materials/news/2015/09",
#  "/materials/news/2015/09/01",
#  "/materials/news/2015/05",
#  "/materials/news/2015/05/15",
#  "/materials/news/2014",
#  "/materials/news/2014/11",
#  "/materials/news/2014/11/26",
#  "/materials/news/2014/11/20",
#  "/materials/news/2013",
#  "/materials/news/2013/09",
#  "/materials/news/2013/09/01",
#  "/materials/news/2011",
#  "/materials/news/2011/03",
#  "/materials/news/2011/03/22",
#  "/materials/news/2010",
#  "/materials/news/2010/12",
#  "/materials/news/2010/12/30",
#  "/materials/news/2010/12/24",
#  "/materials/news/2016/page1",
#  "/materials/news/2016/page2",
