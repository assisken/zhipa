from datetime import datetime
from operator import attrgetter

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render
from django.views.generic import TemplateView

from main.forms import GetGroupScheduleForm, GetTeacherSessionScheduleForm
from main.management.scripts.generate import gen_groups_table, gen_teachers_table
from main.models import FullTimeSchedule, Schedule, ExtramuralSchedule


class GetGroupFulltimeScheduleXlsxView(PermissionRequiredMixin, TemplateView):
    schedule = FullTimeSchedule
    permission_required = 'add_schedule'
    template_name = 'admin/schedule/get_schedule.html'
    render = {
        'form': GetGroupScheduleForm(),
        'opts': FullTimeSchedule._meta,
        'change': False,
        'is_popup': False,
        'save_as': True,
        'has_delete_permission': False,
        'has_add_permission': True,
        'has_change_permission': False,
        'add': True,
        'has_view_permission': True,
        'has_editable_inline_admin_formsets': True,
    }

    @classmethod
    def as_view(cls, **initkwargs):
        cls.render['opts'] = cls.schedule._meta
        return super().as_view(**initkwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.render)

    def post(self, request, *args, **kwargs):
        form = GetGroupScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update({
                'form': form,
                'errors': form.errors,
                'opts': FullTimeSchedule._meta,
            })
            return render(request, self.template_name, self.render)

        groups = form.cleaned_data['groups']
        from_week = form.cleaned_data['from_week']
        try:
            filename = gen_groups_table(groups, from_week)
        except AttributeError:
            form.add_error('groups', 'Превышен максимальный лимит групп')
            self.render.update({
                'form': form,
                'errors': form.errors,
            })
            return render(request, self.template_name, self.render)
        return self._send_xlsx(filename)

    def _send_xlsx(self, filename: str):
        try:
            with open(f'{filename}.xlsx', 'rb') as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{filename}_{date}.xlsx"'.format(
                filename=filename,
                date=datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            )
        except IOError:
            response = HttpResponseNotFound('<h1>File not exist</h1>')

        return response


class GetGroupExtramuralScheduleXlsxView(GetGroupFulltimeScheduleXlsxView):
    schedule = ExtramuralSchedule


class GetTeacherSessionSchedule(GetGroupFulltimeScheduleXlsxView):
    template_name = 'admin/schedule/get_schedule.html'
    render = {
        'form': GetTeacherSessionScheduleForm(),
        'change': False,
        'is_popup': False,
        'save_as': True,
        'has_delete_permission': False,
        'has_add_permission': True,
        'has_change_permission': False,
        'add': True,
        'has_view_permission': True,
        'has_editable_inline_admin_formsets': True,
    }

    @classmethod
    def as_view(cls, **initkwargs):
        cls.schedule = initkwargs.get('schedule')
        return super().as_view(**initkwargs)

    def get(self, request, *args, **kwargs):
        self.render['opts'] = self.schedule._meta
        return render(request, self.template_name, self.render)

    def post(self, request, *args, **kwargs):
        form = GetTeacherSessionScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update({
                'form': form,
                'errors': form.errors,
                'opts': FullTimeSchedule._meta,
            })
            return render(request, self.template_name, self.render)

        schedule_type = form.cleaned_data['schedule_type']
        if schedule_type == Schedule.STUDY:
            return self.__post_study(request, form)
        else:
            return self.__post_session(request, form)

    def __post_study(self, request, form: GetTeacherSessionScheduleForm):
        if not form.is_valid():
            self.render.update({
                'form': form,
                'errors': form.errors,
                'opts': FullTimeSchedule._meta,
            })
            return render(request, self.template_name, self.render)

        teachers = form.cleaned_data['teachers']
        filename = gen_teachers_table(teachers)
        return super()._send_xlsx(filename)

    def __post_session(self, request, form: GetTeacherSessionScheduleForm):
        teachers = form.cleaned_data['teachers']
        items: QuerySet = Schedule.objects.prefetch_related('day', 'groups', 'teachers', 'places') \
            .filter(teachers__in=teachers, schedule_type=Schedule.SESSION)
        _dates = [item.day for item in items if item.day]
        _dates.sort(key=attrgetter('month', 'day'))
        min_date, max_date = _dates[0], _dates[-1]
        dates = ['{:02d}.{:02d}'.format(day, month)
                 for month in range(min_date.month, max_date.month + 1)
                 for day in range(min_date.day, max_date.day)]

        schedule = {
            teacher: {
                '{:02d}.{:02d}'.format(item.day.day, item.day.month): {
                    'name': item.name,
                    'groups': list(item.groups.all()),
                    'place': list(item.places.all()),
                }
            }
            for item in items
            for teacher in item.teachers.all()
            if item.day
        }

        return render(request, 'django/admin/schedule/get_teacher_session_schedule.html', {
            'teachers': teachers,
            'dates': dates,
            'schedule': schedule
        })

