from django.urls import path, register_converter

from .views import *
from . import converters

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitConverter, 'mm')
register_converter(converters.TwoDigitConverter, 'dd')
register_converter(converters.ActivateCodeConverter, 'key')

urlpatterns = [
    path('', NewsListView.as_view()),
    path('news', NewsListView.as_view(), name='news-list'),
    path('news/page<int:number>', NewsListView.as_view(), name='news-list'),
    path('<yyyy:date__year>', NewsDateListView.as_view(), name='news-list'),
    path('<yyyy:date__year>/<mm:date__month>', NewsDateListView.as_view(), name='news-list'),
    path('<yyyy:date__year>/<mm:date__month>/<dd:date__day>', NewsDateListView.as_view(), name='news-list'),

    path('news/id/<int:pk>', NewsDetailView.as_view(), name='news'),
    path('news/<slug:url>', NewsUrlDetailView.as_view(), name='news'),
    path('news/<yyyy:date__year>/<mm:date__month>/<dd:date__day>/<slug:url>',
         NewsDateDetailView.as_view(), name='news'),
]
