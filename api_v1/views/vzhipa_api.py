from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from main.serializers import StudentSerializer
from schedule.serializers import GroupSerializer, SubjectSerializer, TeacherSerializer

Student = apps.get_model(app_label="main", model_name="Student")
Group = apps.get_model(app_label="schedule", model_name="Group")
Teacher = apps.get_model(app_label="schedule", model_name="Teacher")
Subject = apps.get_model(app_label="schedule", model_name="Schedule")


class StudentList(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentRetrieve(RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class GroupList(ListAPIView):
    queryset = Group.objects.prefetch_related("schedule_set", "student_set").all()
    serializer_class = GroupSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ("id", "course", "degree", "study_form")
    ordering_fields = ("id", "course", "degree", "study_form")


class GroupRetrieve(RetrieveAPIView):
    queryset = Group.objects.prefetch_related("schedule_set", "student_set").all()
    serializer_class = GroupSerializer


class TeacherList(ListAPIView):
    queryset = Teacher.objects.prefetch_related("schedule_set").all()
    serializer_class = TeacherSerializer


class TeacherRetrieve(RetrieveAPIView):
    queryset = Teacher.objects.prefetch_related("schedule_set").all()
    serializer_class = TeacherSerializer


class SubjectList(ListAPIView):
    queryset = Subject.objects.prefetch_related("teachers").all()
    serializer_class = SubjectSerializer


class SubjectRetrieve(RetrieveAPIView):
    queryset = Subject.objects.prefetch_related("teachers").all()
    serializer_class = SubjectSerializer
