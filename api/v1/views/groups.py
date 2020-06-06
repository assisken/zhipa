from django.apps import apps
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from schedule.serializers import GroupSerializer


Group = apps.get_model(app_label='schedule', model_name='Group')


class GroupList(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('id', 'course', 'degree', 'study_form')
    ordering_fields = ('id', 'course', 'degree', 'study_form')
