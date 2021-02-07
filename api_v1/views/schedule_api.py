from collections import defaultdict

from django.apps import apps
from rest_framework.response import Response
from rest_framework.views import APIView

from schedule.serializers import (
    ExtramuralScheduleSerializer,
    FulltimeScheduleSerializer,
)
from schedule.views import get_items

Group = apps.get_model(app_label="schedule", model_name="Group")
Schedule = apps.get_model(app_label="schedule", model_name="Schedule")
FullTimeSchedule = apps.get_model(app_label="schedule", model_name="FullTimeSchedule")
ExtramuralSchedule = apps.get_model(
    app_label="schedule", model_name="ExtramuralSchedule"
)


class FullTimeScheduleAPI(APIView):
    group_forms = [form[0] for form in Group.STUDY_FORMS]
    schedule_type = Schedule.STUDY

    def get(self, request, group_id: int):
        group = Group.objects.get(id=group_id)
        filter_cond = {
            "schedule_type": self.schedule_type,
            "group": group,
            "hidden": False,
        }
        items = get_items(schedule=FullTimeSchedule, filter_cond=filter_cond)
        schedule = defaultdict(list)
        for item in items:
            key = "session" if self.schedule_type == Schedule.SESSION else item.week
            schedule[key].append(FulltimeScheduleSerializer(item).data)

        return Response(schedule)


class ExtramuralScheduleAPI(APIView):
    group_forms = [form[0] for form in Group.STUDY_FORMS]
    schedule_type = Schedule.STUDY

    def get(self, request, group_id: int):
        group = Group.objects.get(id=group_id)

        items = (
            ExtramuralSchedule.objects.prefetch_related("teachers")
            .filter(group=group)
            .order_by("name")
        )
        schedule = [ExtramuralScheduleSerializer(item).data for item in items]

        return Response(schedule)
