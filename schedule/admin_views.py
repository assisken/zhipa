import re
from datetime import datetime
from typing import List, Optional, Tuple, Type

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages import add_message
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from schedule.management.scripts.generate import gen_groups_table, gen_teachers_table
from smiap.settings.components.logging import log

from .forms import (
    TEACHER_FORMAT,
    ExtramuralScheduleForm,
    GetGroupScheduleForm,
    GetTeacherSessionScheduleForm,
)
from .models import ExtramuralSchedule, FullTimeSchedule, Schedule, Teacher


class AddExtramuralSchedule(PermissionRequiredMixin, TemplateView):
    """На данной странице возможно добавление сразу нескольких элементов расписания как для сессии, так и для учебного
    времени.

    Group: Выберите, к каким группам привяжется расписание (можно выбрать несколько через Ctrl)
    Schedule type: В каком расписании отобразится вставляемые данные
    Separator: Разделитель столбцов из поля Schedule. Пока неактивен.
    Schedule: Поле, в которые вставляются само расписание по шаблону.

    На данный момент принят следующий шаблон:
    DD.MM DD.MM DD.MM || HH:MM || Предмет || Преподаватель И.О. || Кабинет Площадка
    Нет занятий || совсем || Предмет || Преподаватель И.О. || Кабинет Площадка
    ...

    Поля можно опускать, если хотите оставить пустыми:
    |||| Предмет |||| Кабинет Площадка

    Возможно перечисление нескольких преподавателей:
    DD.MM || HH:MM || Предмет || Иванов И.И, Фёдоров Ф.Ф., Семёнов О.Е. || Кабинет Площадка

    Если кабинет отсутствует, то его можно опустить:
    DD.MM || HH:MM || Предмет || Иванов И.И, Фёдоров Ф.Ф., Семёнов О.Е. || Площадка

    Можно вписывать год занятий, но он будет игнорироваться. Если нужно его добавить, запросите в Trello.
    DD.MM.YYYY || HH:MM || Предмет || Преподаватель И.О. || Площадка
    """

    template_name = "admin/extramural_schedule/add_extramural.html"
    permission_required = "add_schedule"
    render = {
        "description": __doc__,
        "form": ExtramuralScheduleForm(),
        "opts": ExtramuralSchedule._meta,
        "change": False,
        "is_popup": False,
        "save_as": True,
        "has_delete_permission": False,
        "has_add_permission": True,
        "has_change_permission": False,
        "add": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": True,
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.render)

    def post(self, request, *args, **kwargs):
        form = ExtramuralScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update(
                {"form": form, "errors": form.errors, "opts": ExtramuralSchedule._meta}
            )
            return render(request, self.template_name, self.render)

        count = 0
        group: QuerySet = form.cleaned_data["group"]
        schedule_type = form.cleaned_data["schedule_type"]

        for date, time, item, teachers, place in form.schedule_fields():
            try:
                _teachers = self.__get_teachers(teachers)

                schedule, _ = ExtramuralSchedule.objects.get_or_create(
                    date=date,
                    time=time,
                    schedule_type=schedule_type,
                    name=item,
                    group=group,
                    place=place,
                )

                schedule.teachers.set(_teachers)
            except Exception as e:
                log.error(
                    f"Exception was raised. Data:\n{date}\n{time}\n{item}\n{teachers}\n{place}"
                )
                raise e

            count += 1

        ending = "ы" if count > 1 else ""
        add_message(
            request, messages.INFO, f"Предмет{ending} успешно добавлены! ({count} шт.)"
        )
        return HttpResponseRedirect("../")

    @staticmethod
    def __get_teachers(teachers: Tuple[str, ...]) -> Tuple[Optional[Teacher], ...]:
        if not teachers:
            return tuple()

        out: List[Teacher] = []
        regex = re.compile(TEACHER_FORMAT)
        for teacher in teachers:
            if not teacher:
                continue

            match = regex.match(teacher)
            if not match:
                raise ValueError(f"Matches did not found at teacher: {teacher}")

            db_teacher = Teacher.objects.filter(
                lastname=match.group("lastname"),
                firstname__startswith=match.group("firstname"),
                middlename__startswith=match.group("middlename"),
            ).first()
            if db_teacher is None:
                db_teacher = Teacher.objects.create(
                    lastname=match.group("lastname"),
                    firstname=match.group("firstname"),
                    middlename=match.group("middlename"),
                )
            out.append(db_teacher)
        return tuple(out)


class GetGroupFulltimeScheduleXlsxView(PermissionRequiredMixin, TemplateView):
    schedule: Type[Schedule] = FullTimeSchedule
    permission_required = "add_schedule"
    template_name = "admin/schedule/get_schedule.html"
    render = {
        "form": GetGroupScheduleForm(),
        "opts": FullTimeSchedule._meta,
        "change": False,
        "is_popup": False,
        "save_as": True,
        "has_delete_permission": False,
        "has_add_permission": True,
        "has_change_permission": False,
        "add": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": True,
    }

    @classmethod
    def as_view(cls, **initkwargs):
        cls.render["opts"] = cls.schedule._meta
        return super().as_view(**initkwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.render)

    def post(self, request, *args, **kwargs):
        form = GetGroupScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update(
                {"form": form, "errors": form.errors, "opts": FullTimeSchedule._meta}
            )
            return render(request, self.template_name, self.render)

        groups = form.cleaned_data["groups"]
        from_week = form.cleaned_data["from_week"]
        try:
            filename = gen_groups_table(groups, from_week, "group_template.xlsx")
        except AttributeError:
            form.add_error("groups", "Превышен максимальный лимит групп")
            self.render.update({"form": form, "errors": form.errors})
            return render(request, self.template_name, self.render)
        return self._send_xlsx(filename)

    def _send_xlsx(self, filename: str):
        try:
            with open(f"{filename}.xlsx", "rb") as f:
                file_data = f.read()
            response = HttpResponse(file_data, content_type="application/vnd.ms-excel")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="{filename}_{date}.xlsx"'.format(
                filename=filename, date=datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            )
        except IOError:
            response = HttpResponseNotFound("<h1>File not exist</h1>")

        return response


class GetGroupExtramuralScheduleXlsxView(GetGroupFulltimeScheduleXlsxView):
    schedule = ExtramuralSchedule


class GetTeacherSessionSchedule(GetGroupFulltimeScheduleXlsxView):
    template_name = "admin/schedule/get_schedule.html"
    render = {
        "form": GetTeacherSessionScheduleForm(),
        "change": False,
        "is_popup": False,
        "save_as": True,
        "has_delete_permission": False,
        "has_add_permission": True,
        "has_change_permission": False,
        "add": True,
        "has_view_permission": True,
        "has_editable_inline_admin_formsets": True,
    }

    @classmethod
    def as_view(cls, **initkwargs):
        cls.schedule = initkwargs.get("schedule")
        return super().as_view(**initkwargs)

    def get(self, request, *args, **kwargs):
        self.render["opts"] = self.schedule._meta
        return render(request, self.template_name, self.render)

    def post(self, request, *args, **kwargs):
        form = GetTeacherSessionScheduleForm(request.POST)
        if not form.is_valid():
            self.render.update(
                {"form": form, "errors": form.errors, "opts": FullTimeSchedule._meta}
            )
            return render(request, self.template_name, self.render)

        schedule_type = form.cleaned_data["schedule_type"]
        teachers = form.cleaned_data["teachers"]
        filename = gen_teachers_table(teachers, schedule_type, "teacher_template.xlsx")
        return super()._send_xlsx(filename)
