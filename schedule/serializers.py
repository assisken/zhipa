from rest_framework import serializers

from .models import Group, Day, Teacher, FullTimeSchedule, ExtramuralSchedule


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'course', 'degree', 'study_form', 'study_until_week')


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ('day', 'month', 'week_day')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('lastname', 'firstname', 'middlename')


class FulltimeScheduleSerializer(serializers.ModelSerializer):
    places = serializers.SerializerMethodField()
    day = DaySerializer(many=False, read_only=True)
    teachers = TeacherSerializer(many=True, read_only=True)

    class Meta:
        model = FullTimeSchedule
        fields = ('day', 'starts_at', 'ends_at', 'item_type', 'schedule_type', 'name', 'teachers', 'places')

    def get_places(self, obj: Meta.model):
        return [str(place) for place in obj.places.all()]


class ExtramuralScheduleSerializer(serializers.ModelSerializer):
    places = serializers.SerializerMethodField()
    teachers = TeacherSerializer(many=True, read_only=True)

    class Meta:
        model = ExtramuralSchedule
        fields = ('day', 'time', 'schedule_type', 'name', 'teachers', 'places')

    def get_places(self, obj: Meta.model):
        return [str(place) for place in obj.places.all()]
