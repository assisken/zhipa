from django.urls import path
from main.views import News
from main.views.schedule import ScheduleIndex

urlpatterns = [
    path('', News.as_view(), name='news'),
    path('materials/timetable/', ScheduleIndex.as_view(), name='schedule'),
]
