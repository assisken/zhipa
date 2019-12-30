import re
from collections import defaultdict

from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Group, FullTimeSchedule, Teacher, Schedule
from utils.date import TeachTime, TeachState


class GroupTimetableView(TemplateView):
    template_name = "materials/timetable/index.html"
    schedule = FullTimeSchedule
    schedule_type = Schedule.TEACHING

    @classmethod
    def as_view(cls, **initkwargs):
        cls.schedule = initkwargs.get('schedule')
        cls.schedule_type = initkwargs.get('schedule_type')
        return super().as_view(**initkwargs)

    def get(self, request, *args, **kwargs):
        teach_time = TeachTime()

        groups = Group.objects.only('name').filter(study_form=self.schedule.objects.study_form)
        group_name = request.GET.get('group', groups.first().name)
        show_weeks = self.schedule_type == Schedule.TEACHING and self.schedule == FullTimeSchedule

        if show_weeks:
            week = request.GET.get('week', teach_time.week)
        else:
            week = None

        group = Group.objects.get(name=group_name)
        items = self.schedule.objects.prefetch_related('day', 'places', 'teachers') \
            .filter(schedule_type=self.schedule_type, day__week=week, groups__exact=group) \
            .order_by('day__month', 'day__day', 'starts_at')
        schedule = defaultdict(list)
        for item in items:
            schedule[item.day].append(item)

        if len(groups) > 0:
            weeks = teach_time.weeks_in_semester
        else:
            weeks = 0

        return render(request, self.template_name, {
            'groups': groups,
            'group_name': group_name,
            'show_weeks': show_weeks,
            'weeks': weeks,
            'week': week,
            'schedule': schedule,
            'date_block': date_block(teach_time),
            'course': group.course if group_name else 0,
            'study_forms': Group.objects.order_by('-study_form').values_list('study_form').distinct(),
            'session': self.schedule_type == Schedule.SESSION
        })


def date_block(teach_time: TeachTime):
    teach_state = teach_time.teach_state
    if teach_state.it_is(TeachState.SEMESTER):
        return {
            'text': 'Учёба продолжается',
            'num': teach_time.week,
            'desc': 'неделя'
        }
    elif teach_state.it_is(TeachState.HOLIDAYS):
        return {
            'text': 'Начало учёбы',
            'num': teach_time.next_start.day,
            'desc': teach_time.next_start.strftime('%B')
        }

    return {
        'text': '',
        'num': '404',
        'desc': 'Not Found'
    }


class TeacherTimetableView(TemplateView):
    template_name = 'materials/timetable/teachers.html'

    def get(self, request, *args, **kwargs):
        teach_time = TeachTime()

        teachers = Teacher.objects.filter(staff__isnull=False).order_by('lastname', 'firstname', 'middlename')
        teacher_name = request.GET.get('teacher', str(teachers[0]))
        lastname, firstname, middlename, *_ = re.split('[ .]', teacher_name, maxsplit=3)
        teacher = Teacher.objects.get(lastname=lastname,
                                      firstname__startswith=firstname,
                                      middlename__startswith=middlename)
        week = request.GET.get('week',
                               teach_time.week if teach_time.week <= teach_time.weeks_in_semester else teach_time.week)
        items = FullTimeSchedule.objects.prefetch_related('day', 'groups', 'teachers', 'places') \
            .filter(day__week=week, teachers__exact=teacher)\
                                .order_by('day__date', 'starts_at')
        schedule = defaultdict(list)
        for item in items:
            schedule[item.day].append(item)

        if len(teachers) > 0:
            weeks = teach_time.weeks_in_semester
        else:
            weeks = 0

        return render(request, self.template_name, {
            'teachers': teachers,
            'teacher': teacher,
            'weeks': weeks,
            'week': week,
            'schedule': schedule,
            'date_block': date_block(teach_time)
        })
