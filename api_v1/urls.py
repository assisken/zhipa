from django.apps import apps
from django.urls import path

from .views.vzhipa_api import (
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
]
