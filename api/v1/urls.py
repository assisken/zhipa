from django.apps import apps
from django.urls import path

from api.v1.views.groups import GroupList
from api.v1.views.schedule_api import ExtramuralScheduleAPI, FullTimeScheduleAPI

Schedule = apps.get_model(app_label="schedule", model_name="Schedule")

urlpatterns = [
    path("groups/", GroupList.as_view(), name="groups"),
    path(
        "schedule/fulltime/study/<int:group_id>",
        FullTimeScheduleAPI.as_view(schedule_type=Schedule.STUDY),
        name="schedule-study",
    ),
    path(
        "schedule/fulltime/session/<int:group_id>",
        FullTimeScheduleAPI.as_view(schedule_type=Schedule.SESSION),
        name="schedule-session",
    ),
    path(
        "schedule/extramural/study/<int:group_id>",
        ExtramuralScheduleAPI.as_view(schedule_type=Schedule.STUDY),
        name="schedule-study",
    ),
    path(
        "schedule/extramural/session/<int:group_id>",
        ExtramuralScheduleAPI.as_view(schedule_type=Schedule.SESSION),
        name="schedule-session",
    ),
]
