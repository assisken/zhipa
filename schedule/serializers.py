from rest_framework import serializers

from .models import ExtramuralSchedule, FullTimeSchedule, Group, Teacher


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name", "course", "degree", "study_form", "study_until_week")


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("lastname", "firstname", "middlename")


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
        fields = ("date", "time", "schedule_type", "name", "teachers", "place")
