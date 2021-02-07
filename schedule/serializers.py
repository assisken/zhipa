from django.apps import apps
from rest_framework import serializers

from .models import ExtramuralSchedule, FullTimeSchedule, Group, Schedule, Teacher

Student = apps.get_model(app_label="main", model_name="Student")


class StudentIdSerializer(serializers.ModelSerializer):
    def to_representation(self, instance) -> int:
        return instance.pk

    class Meta:
        model = Student


class SubjectIdSerializer(serializers.ModelSerializer):
    def to_representation(self, instance: Schedule) -> int:
        return instance.pk

    class Meta:
        model = Schedule


class GroupSerializer(serializers.ModelSerializer):
    subjects = StudentIdSerializer(source="schedule_set", many=True, read_only=True)
    students = StudentIdSerializer(source="student_set", many=True, read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name", "subjects", "students")
        read_only_fields = ("id", "name", "subjects", "students")
        depth = 1


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "lastname", "firstname", "middlename")
        read_only_fields = ("id", "lastname", "firstname", "middlename")


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ("id", "name", "group", "teachers")
        read_only_fields = ("id", "name", "group", "teachers")


class FulltimeScheduleSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)

    class Meta:
        model = FullTimeSchedule
        fields = (
            "date",
            "time",
            "item_type",
            "schedule_type",
            "name",
            "teachers",
            "place",
        )


class ExtramuralScheduleSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)

    class Meta:
        model = ExtramuralSchedule
        fields = (
            "date",
            "time",
            "name",
            "place",
            "teachers",
            "schedule_type",
        )
