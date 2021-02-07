from django.apps import apps
from django.urls import path

from .views.schedule_api import ExtramuralScheduleAPI, FullTimeScheduleAPI
from .views.vzhipa_api import (
    ContainersList,
    ContainersRetrieve,
    GroupList,
    GroupRetrieve,
    StudentList,
    StudentRetrieve,
    SubjectList,
    SubjectRetrieve,
    TeacherList,
    TeacherRetrieve,
)

Schedule = apps.get_model(app_label="schedule", model_name="Schedule")

urlpatterns = [
    path("students/", StudentList.as_view(), name="students"),
    path("students/<int:pk>", StudentRetrieve.as_view(), name="students"),
    path("groups/", GroupList.as_view(), name="groups"),
    path("groups/<int:pk>", GroupRetrieve.as_view(), name="groups"),
    path("teachers/", TeacherList.as_view(), name="teachers"),
    path("teachers/<int:pk>", TeacherRetrieve.as_view(), name="teachers"),
    path("subjects/", SubjectList.as_view(), name="subjects"),
    path("subjects/<int:pk>", SubjectRetrieve.as_view(), name="subjects"),
    path("containers/", ContainersList.as_view(), name="containers"),
    path("containers/<int:pk>", ContainersRetrieve.as_view(), name="containers"),
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
