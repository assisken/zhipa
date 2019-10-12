import os
from math import ceil

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F
from django.urls import reverse

from utils import group


class User(AbstractUser):
    pass


def get_news_image_path(instance: 'News', filename: str):
    return os.path.join('news', instance.date.strftime('%Y%m%d'), filename)


class News(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    url = models.CharField(max_length=60, blank=True, default='')
    img = models.ImageField(max_length=120, blank=True, default='',
                            upload_to=get_news_image_path)
    description = models.TextField()
    text = models.TextField()
    hidden = models.BooleanField(default=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-pk']

    def __str__(self):
        return self.title

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
    study_form = models.CharField(max_length=12, choices=STUDY_FORMS, null=False, blank=False)
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
        return max(map(int, self.schedule.keys()))


def get_profile_image_path(instance: 'Profile', filename: str):
    return os.path.join('profile', str(instance.pk), filename)


class Profile(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    img = models.ImageField(max_length=60, null=True,
                            default=None, upload_to=get_profile_image_path, blank=True)

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.middlename}'


class Staff(Profile):
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
        # proxy = True

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.middlename}'


class Student(Profile):
    group_name = models.CharField(max_length=50)


class Teacher(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        try:
            self.staff = Staff.objects.get(lastname=self.lastname, firstname=self.firstname, middlename=self.middlename)
        except Staff.DoesNotExist:
            self.staff = None
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} {}.{}.'.format(self.lastname, self.firstname[0], self.middlename[0])


class Place(models.Model):
    building = models.TextField()
    number = models.TextField(null=True)

    def __str__(self):
        if self.number:
            return '{} {}'.format(self.building, self.number)
        else:
            return self.building


class Day(models.Model):
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    week_day = models.CharField(max_length=2)
    week = models.IntegerField()

    def __str__(self):
        return '{} ({:02d}.{:02d})'.format(self.week_day, self.day, self.month)


class Item(models.Model):
    LECTION = 'ЛК'
    PRACTICE = 'ПЗ'
    LABWORK = 'ЛР'
    CONTROL = 'КСР'

    ITEM_TYPES = [
        (LECTION, 'ЛК'),
        (PRACTICE, 'ПЗ'),
        (LABWORK, 'ЛР'),
        (CONTROL, 'КСР')
    ]

    starts_at = models.TimeField()
    ends_at = models.TimeField()
    type = models.CharField(max_length=3, choices=ITEM_TYPES)
    name = models.TextField()
    places = models.ManyToManyField(Place)
    teachers = models.ManyToManyField(Teacher)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)


class Publication(models.Model):
    name = models.TextField(blank=False, null=False)
    place = models.TextField(blank=False, null=False)
    authors = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.name
