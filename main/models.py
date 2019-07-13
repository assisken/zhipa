import os
import re
from datetime import datetime
from math import ceil

from django.db import models
from django.db.models import F
from django.contrib.postgres import fields
from django.urls import reverse

from main.types import Degree
from utils import group


def get_image_path():
    return os.path.join('images', 'lecturers')


class Staff(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    img = models.ImageField(max_length=60, null=True,
                            default=None, upload_to=get_image_path(), blank=True)
    regalia = models.CharField(max_length=60)
    description = models.TextField(null=True, default=None, blank=True)
    leader = models.BooleanField(default=False)
    lecturer = models.BooleanField(default=True)
    hide = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Staff'
        ordering = [F('leader').desc(),
                    F('lecturer').desc(),
                    F('hide').asc(),
                    F('lastname').asc(),
                    F('firstname').asc(),
                    F('middlename').asc(),
                    F('pk').asc()]

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.middlename}'


class News(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    url = models.CharField(max_length=60, blank=True, default='')
    img = models.ImageField(max_length=120, blank=True, default='')
    description = models.TextField()
    text = models.TextField()
    hidden = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-pk']

    def get_url(self):
        if self.url:
            kwargs = {
                'year': str(self.date.year).zfill(4),
                'month': str(self.date.month).zfill(2),
                'day': str(self.date.day).zfill(2),
                'url': self.url
            }
            return reverse('news-date-url', kwargs=kwargs)
        return reverse('news', kwargs={'pk': self.pk})


class Group(models.Model):
    FULL_TIME = 'очная'
    PART_TIME = 'очно-заочная'
    EXTRAMURAL = 'заочная'

    STUDY_FORMS = [
        (FULL_TIME, 'очная'),
        (PART_TIME, 'очно-заочная'),
        (EXTRAMURAL, 'заочная')
    ]

    name = models.CharField(max_length=25, unique=True, null=False, blank=False)
    course = models.PositiveSmallIntegerField(null=False, editable=False)
    degree = models.PositiveSmallIntegerField(null=False, editable=False)
    semester = models.PositiveSmallIntegerField(null=False, blank=False)
    study_form = models.CharField(max_length=12, choices=None, null=False, blank=False)
    schedule = fields.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.course = ceil(self.semester / 2)
        self.degree = group.degree(self.name).value
        super().save(*args, **kwargs)

    def weeks(self) -> int:
        return max(map(int, self.schedule.keys()))
