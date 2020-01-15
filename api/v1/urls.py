from django.urls import path

from api.v1.views import *
from main.models import Schedule

urlpatterns = [
    path('groups/', GroupList.as_view(), name='groups'),
    path('schedule/study/<int:group_id>',
         ScheduleAPI.as_view(schedule_type=Schedule.STUDY), name='schedule-study'),
    path('schedule/session/<int:group_id>',
         ScheduleAPI.as_view(schedule_type=Schedule.SESSION), name='schedule-session')
]
