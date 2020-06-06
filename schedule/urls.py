from django.urls import path

from .views import *

urlpatterns = [
    # Timetable
    path('timetable',
         GroupTimetableView.as_view(schedule=FullTimeSchedule, schedule_type=Schedule.STUDY),
         name='timetable'),
    path('timetable/extramural',
         ExtramuralGroupTimetableView.as_view(schedule=ExtramuralSchedule, schedule_type=Schedule.STUDY),
         name='timetable-extramural'),
    path('session',
         GroupTimetableView.as_view(schedule=FullTimeSchedule, schedule_type=Schedule.SESSION),
         name='timetable-session'),
    path('timetable/ex-session',
         ExtramuralGroupTimetableView.as_view(schedule=ExtramuralSchedule, schedule_type=Schedule.SESSION),
         name='timetable-extramural-session'),

    # Deprecated: https://trello.com/c/I7ygJ9Nk
    path('timetable/teacher', TeacherTimetableView.as_view(), name='timetable-teacher'),
]
