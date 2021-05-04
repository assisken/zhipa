import re
from typing import List

from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.core.exceptions import ValidationError

from .models import ExtramuralSchedule, Group, Schedule, Teacher


class GeneralForm(forms.Form):
    error_css_class = "errors"
    required_css_class = "required"


TEACHER_FORMAT = r"^(?P<lastname>[А-Яа-яЁё]+) (?P<firstname>[А-Яа-яЁё])\.(?P<middlename>[А-Яа-яЁё])\.$"


def check_columns_count(value: str):
    count = 5
    items = value.split("\n")
    for line, item in enumerate(items):
        col_count = item.count("||") + 1
        if col_count != count:
            raise ValidationError(
                f"Требуется {count} столбцов, но было получено {col_count} столбцов.\n"
                f"Строка: {line + 1}"
            )


def parse_columns(func):
    def wrapper(value: str):
        pattern = re.compile(
            r"(?P<date>.*)\|\|(?P<time>.*)\|\|(?P<item>.*)\|\|(?P<teacher>.*)\|\|(?P<place>.*)"
        )
        kwargs = {
            "dates": (x.group("date").strip() for x in pattern.finditer(value)),
            "times": (x.group("time").strip() for x in pattern.finditer(value)),
            "items": (x.group("item").strip() for x in pattern.finditer(value)),
            "teachers": (x.group("teacher").strip() for x in pattern.finditer(value)),
            "places": (x.group("place").strip() for x in pattern.finditer(value)),
        }

        return func(**kwargs)

    return wrapper


@parse_columns
def check_teacher_abbreviation_format(teachers, **kwargs):
    for line, teacher in enumerate(teachers):
        if not re.match(TEACHER_FORMAT, teacher) and teacher != "":
            raise ValidationError(
                'Преподаватель должен быть оформлен в формате "Фамилия И.О." Например: Иванов И.И.\n'
                "Возможно перечисление преподавателей, которое нужно оформить в формате "
                '"Фамилия1 И.О., Фамилия2 И.О., ...". Например:\n'
                "Иванов И.И., Петров П.П., Семёнов С.С.\n"
                "Также возможно опустить данный столбец (оставить пустым)\n"
                f'Строка {line + 1}, значение: "{teacher}"'
            )


class ExtramuralScheduleForm(GeneralForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(study_form=Group.EXTRAMURAL),
        required=True,
    )
    schedule_type = forms.ChoiceField(choices=ExtramuralSchedule.SCHEDULE_TYPES)
    separator = forms.CharField(initial="||", disabled=True)
    schedule = forms.CharField(
        widget=forms.Textarea(attrs={"class": "vLargeTextField"}),
        validators=(
            check_columns_count,
            check_teacher_abbreviation_format,
        ),
    )

    def schedule_fields(self):
        data = self.cleaned_data["schedule"]
        separator = self.cleaned_data["separator"]
        for line in data.splitlines():
            date, time, item, teachers, place = line.split(separator, maxsplit=4)
            date = date.strip()
            time = time.strip()
            item = item.strip()
            _teachers = tuple(teacher.strip() for teacher in teachers.split(", "))
            place = place.strip()

            yield date, time, item, _teachers, place


def check_max_group_count(value: List[str]):
    minimum = 1
    maximum = 16
    count = len(value)
    if count > maximum or count < minimum:
        raise ValidationError(f"Пожалуйста, выберите от {minimum} до {maximum} групп")


def check_max_teacher_count(value: List[str]):
    minimum = 1
    maximum = 16
    count = len(value)
    if count > maximum or count < minimum:
        raise ValidationError(
            f"Пожалуйста, выберите от {minimum} до {maximum} преподавателей"
        )


class GetGroupScheduleForm(GeneralForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by("-study_form", "degree", "semester", "name"),
        required=True,
        initial=Group.objects.filter(study_form=Group.FULL_TIME),
        validators=(check_max_group_count,),
    )
    from_week = forms.IntegerField(min_value=1, max_value=17)


class GetTeacherSessionScheduleForm(GeneralForm):
    teachers = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        required=True,
        initial=Teacher.objects.filter(staff__isnull=False),
        validators=(check_max_teacher_count,),
    )
    schedule_type = forms.ChoiceField(
        choices=Schedule.SCHEDULE_TYPES, required=True, initial=Schedule.STUDY
    )


class GetTeacherScheduleForm(GeneralForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        required=True,
        widget=admin_widgets.FilteredSelectMultiple(
            verbose_name=Teacher._meta.verbose_name or "Teacher", is_stacked=False
        ),
    )
