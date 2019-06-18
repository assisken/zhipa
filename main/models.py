import os
from datetime import datetime

from django.db import models
from django.db.models import F
from django.contrib.postgres import fields
from django.urls import reverse


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
    date = models.DateTimeField(auto_now=True)
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
                'year': self.date.year,
                'month': self.date.month,
                'day': self.date.day,
                'url': self.url
            }
            return reverse('news-date-url', kwargs=kwargs)
        return reverse('news', kwargs={'pk': self.pk})


class Group(models.Model):
    name = models.CharField(max_length=25, unique=True, null=False, blank=False)
    schedule = fields.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    def weeks(self):
        return max(map(int, self.schedule.keys()))

    def course(self):
        year = int(self.name.split('-')[-1])  # Get year from name of group
        now = datetime.now()
        course = now.year % 100 - year
        if now.month >= 9:                    # Study time starts from September. So course must be increased
            course += 1
        return course
