from math import ceil
from typing import Optional

from django.apps import apps
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import Max

from main.utils import group


class Group(models.Model):
    FULL_TIME = "очная"
    PART_TIME = "очно-заочная"
    EXTRAMURAL = "заочная"

    STUDY_FORMS = [
        (FULL_TIME, "очная"),
        (PART_TIME, "очно-заочная"),
        (EXTRAMURAL, "заочная"),
    ]

    name = models.CharField(max_length=25, unique=True, null=False, blank=False)
    course = models.PositiveSmallIntegerField(null=False, editable=False)
    degree = models.PositiveSmallIntegerField(null=False, editable=False)
    semester = models.PositiveSmallIntegerField(null=False, blank=False)
    study_form = models.CharField(
        max_length=12, choices=STUDY_FORMS, null=False, blank=False
    )
    schedule_version = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.course = ceil(self.semester / 2)
        if not self.degree:
            self.degree = group.degree(self.name).value
        if not self.study_form:
            self.study_form = group.study_form(self.name)
        super().save(*args, **kwargs)

    def weeks(self) -> int:
        return self.schedule_set.count()

    @property
    def study_until_week(self) -> Optional[int]:
        try:
            return self.schedule_set.aggregate(Max("day__week"))["day__week__max"]
        except FieldError:
            return None

    class Meta:
        ordering = ("degree", "course", "-study_form", "name")


class Teacher(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    staff = models.OneToOneField("main.Staff", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("lastname", "firstname", "middlename")

    def save(self, *args, **kwargs):
        Staff = apps.get_model(app_label="main", model_name="Staff")
        staff = Staff.objects.filter(
            lastname=self.lastname, firstname=self.firstname, middlename=self.middlename
        )
        if len(staff) != 0:
            self.staff = staff[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} {}.{}.".format(self.lastname, self.firstname[0], self.middlename[0])


class Place(models.Model):
    building = models.TextField()
    number = models.TextField(null=True)

    def __str__(self):
        if self.number:
            return "{} {}".format(self.building, self.number)
        else:
            return self.building

    class Meta:
        ordering = ("building", "number", "pk")


class Day(models.Model):
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    week_day = models.CharField(max_length=2, blank=True)
    week = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} ({:02d}.{:02d})".format(self.week_day, self.day, self.month)

    class Meta:
        ordering = ("month", "day")


class Schedule(models.Model):
    STUDY = "Учебн."
    SESSION = "Сессия"

    SCHEDULE_TYPES = [(STUDY, "Учебное время"), (SESSION, "Сессия")]

    schedule_type = models.CharField(
        max_length=6, choices=SCHEDULE_TYPES, default=STUDY, null=True
    )
    name = models.TextField(null=True)
    places = models.ManyToManyField(Place)
    teachers = models.ManyToManyField(Teacher)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return str(self)


class FullTimeSchedule(Schedule):
    LECTION = "ЛК"
    PRACTICE = "ПЗ"
    LABWORK = "ЛР"
    CONTROL = "КСР"
    EXAM = "Экз"
    EMPTY = ""

    ITEM_TYPES = [
        (LECTION, "ЛК"),
        (PRACTICE, "ПЗ"),
        (LABWORK, "ЛР"),
        (CONTROL, "КСР"),
        (EXAM, "Экзамен"),
        (EMPTY, "Оставить пустым"),
    ]

    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, blank=True)
    starts_at = models.TimeField(null=True, blank=True)
    ends_at = models.TimeField(null=True, blank=True)
    item_type = models.CharField(
        max_length=3, choices=ITEM_TYPES, default=EMPTY, blank=True
    )

    def key(self):
        return f"{self.starts_at.isoformat()} {self.ends_at.isoformat()} {str(self.day)} {self.name} {self.item_type}"

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()} [Очное])"

    class Meta:
        verbose_name_plural = "Fulltime Schedule"


class ExtramuralSchedule(Schedule):
    day = models.TextField(null=True, blank=True)
    time = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} [Заочное]"

    class Meta:
        verbose_name_plural = "Extramural Schedule"
