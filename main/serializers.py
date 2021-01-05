from rest_framework import serializers

from main.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("id", "firstname", "lastname", "middlename", "group")
        read_only_fields = ("id", "firstname", "lastname", "middlename", "group")
