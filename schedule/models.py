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
            return self.schedule_set.aggregate(Max("week"))["week__max"]
        except FieldError:
            return None

    class Meta:
        ordering = ("degree", "course", "-study_form", "name")


class Teacher(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    staff = models.ForeignKey("main.Staff", on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("lastname", "firstname", "middlename")

    def get_absolute_url(self):
        if self.staff:
            return self.staff.get_absolute_url()

    def save(self, *args, **kwargs):
        Staff = apps.get_model(app_label="main", model_name="Staff")
        staff = Staff.objects.filter(
            lastname=self.lastname, firstname=self.firstname, middlename=self.middlename
        )
        if len(staff) != 0:
            self.staff = staff[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} {}.{}.".format(
            self.lastname,
            self.firstname[0] if self.firstname else "",
            self.middlename[0] if self.middlename else "",
        )


class Schedule(models.Model):
    STUDY = "Учебн."
    SESSION = "Сессия"

    SCHEDULE_TYPES = [(STUDY, "Учебное время"), (SESSION, "Сессия")]

    schedule_type = models.CharField(
        max_length=6, choices=SCHEDULE_TYPES, default=STUDY, null=True
    )
    date = models.TextField(null=False, blank=True, default="")
    time = models.TextField(null=False, blank=True, default="")
    name = models.TextField(null=False, blank=True, default="")
    place = models.TextField(null=False, blank=True)
    teachers = models.ManyToManyField(Teacher)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    hidden = models.BooleanField(default=True)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"[{self.schedule_type}] ({self.date}, {self.time}) {self.group.name} - {self.name}"


class FullTimeSchedule(Schedule):
    week_day = models.TextField(null=False, blank=True)
    week = models.IntegerField(null=True, blank=True)
    item_type = models.CharField(max_length=10, blank=True, null=False)

    def key(self):
        return f"{self.time} {str(self.date)} {self.name} {self.item_type}"

    def __str__(self):
        return f"{self.name} ({self.item_type} [Очное])"

    class Meta:
        verbose_name_plural = "Fulltime Schedule"


class ExtramuralSchedule(Schedule):
    def __str__(self):
        return f"{self.name} [Заочное]"

    class Meta:
        verbose_name_plural = "Extramural Schedule"
