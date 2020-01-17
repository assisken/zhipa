from collections import defaultdict

from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import ScheduleSerializer
from main.models import Group, Schedule
from main.views.timetable_view import get_items


class ScheduleAPI(APIView):
    group_forms = [form[0] for form in Group.STUDY_FORMS]
    schedule_type = Schedule.STUDY

    def get(self, request, group_id: int):
        group = Group.objects.get(id=group_id)
        filter_cond = {
            'schedule_type': self.schedule_type,
            'groups__exact': group
        }
        if self.schedule_type == Schedule.STUDY:
            filter_cond['day__week__in'] = range(1, group.study_until_week + 1)

        items = get_items(schedule=Schedule, filter_cond=filter_cond)
        schedule = defaultdict(list)
        for item in items:
            key = 'session' if self.schedule_type == Schedule.SESSION else item.day.week
            schedule[key].append(ScheduleSerializer(item).data)

        return Response(schedule)
