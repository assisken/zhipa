import os
from math import ceil
from typing import Optional

from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import Max
from django.urls import reverse

from main.utils.date import get_year_from_string
from main.validators import validate_news_content_image_begin_name_with_a_letter
from main.utils import group


class User(AbstractUser):
    pass


def get_news_cover_path(instance: 'NewsCover', filename: str):
    return os.path.join('news', instance.news.date.strftime('%Y%m%d'), 'cover.jpg')


def get_news_content_image_path(instance: 'NewsContentImage', filename: str):
    return os.path.join('news', instance.news.date.strftime('%Y%m%d'), filename)


class News(models.Model):
    HTML = 'html'
    MARKDOWN = 'md'

    RENDERS = [
        (HTML, 'html'),
        (MARKDOWN, 'markdown')
    ]

    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    url = models.CharField(max_length=60, blank=True, default=None, null=True, unique=True)
    cover = models.ImageField(max_length=120, blank=True, default='', upload_to=get_news_cover_path,)
    description = models.TextField()
    text = models.TextField()
    render_in = models.CharField(max_length=8, choices=RENDERS, null=False, blank=False, default=HTML)
    hidden = models.BooleanField(default=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)

    class Meta:
        verbose_name_plural = 'News'
        ordering = ('-pk',)

    def __str__(self):
        return self.title

    def news_cover(self) -> Optional['NewsCover']:
        covers = self.newscover_set.all()
        if len(covers) == 0:
            return None
        return covers.first()

    def get_url(self):
        if self.url:
            kwargs = {
                'url': self.url
            }
            return reverse('news-url', kwargs=kwargs)
        return reverse('news', kwargs={'pk': self.pk})


class NewsCover(models.Model):
    img = models.ImageField(max_length=120, blank=True, default='', upload_to=get_news_cover_path)
    content = models.CharField(max_length=60, null=True, blank=True, default=None)
    color = ColorField(default='#0997ef')
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=False, blank=False)


class NewsContentImage(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False,
                            validators=(validate_news_content_image_begin_name_with_a_letter,))
    img = models.ImageField(max_length=120, blank=True, default='', upload_to=get_news_content_image_path)
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, blank=False)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.name} ({self.img.name})'


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
        return self.schedule_set.count()

    @property
    def study_until_week(self) -> Optional[int]:
        try:
            return self.schedule_set.aggregate(Max('day__week'))['day__week__max']
        except FieldError:
            return

    class Meta:
        ordering = ('degree', 'course', '-study_form', 'name')


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
        ordering = ('-leader', '-lecturer', 'hide', 'lastname', 'firstname', 'middlename', 'pk')

    def __str__(self):
        return f'{self.lastname} {self.firstname} {self.middlename}'


class Student(Profile):
    group_name = models.CharField(max_length=50)


class Teacher(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ('lastname', 'firstname', 'middlename')

    def save(self, *args, **kwargs):
        staff = Staff.objects.filter(lastname=self.lastname, firstname=self.firstname, middlename=self.middlename)
        if len(staff) != 0:
            self.staff = staff[0]
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

    class Meta:
        ordering = ('building', 'number', 'pk')


class Day(models.Model):
    day = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    week_day = models.CharField(max_length=2, blank=True)
    week = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{} ({:02d}.{:02d})'.format(self.week_day, self.day, self.month)

    class Meta:
        ordering = ('month', 'day')


class Schedule(models.Model):
    STUDY = 'Учебн.'
    SESSION = 'Сессия'

    SCHEDULE_TYPES = [
        (STUDY, 'Учебное время'),
        (SESSION, 'Сессия')
    ]

    schedule_type = models.CharField(max_length=6, choices=SCHEDULE_TYPES, default=STUDY, null=True)
    name = models.TextField(null=True)
    places = models.ManyToManyField(Place)
    teachers = models.ManyToManyField(Teacher)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __repr__(self):
        return str(self)


class FullTimeSchedule(Schedule):
    LECTION = 'ЛК'
    PRACTICE = 'ПЗ'
    LABWORK = 'ЛР'
    CONTROL = 'КСР'
    EXAM = 'Экз'
    EMPTY = ''

    ITEM_TYPES = [
        (LECTION, 'ЛК'),
        (PRACTICE, 'ПЗ'),
        (LABWORK, 'ЛР'),
        (CONTROL, 'КСР'),
        (EXAM, 'Экзамен'),
        (EMPTY, 'Оставить пустым'),
    ]

    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True, blank=True)
    starts_at = models.TimeField(null=True, blank=True)
    ends_at = models.TimeField(null=True, blank=True)
    item_type = models.CharField(max_length=3, choices=ITEM_TYPES, default=EMPTY, blank=True)

    def key(self):
        return f'{self.starts_at.isoformat()} {self.ends_at.isoformat()} {str(self.day)} {self.name} {self.item_type}'

    def __str__(self):
        return f'{self.name} ({self.get_item_type_display()} [Очное])'

    class Meta:
        verbose_name_plural = 'Fulltime Schedule'


class ExtramuralSchedule(Schedule):
    day = models.TextField(null=True, blank=True)
    time = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} [Заочное]'

    class Meta:
        verbose_name_plural = 'Extramural Schedule'


class Publication(models.Model):
    name = models.TextField(blank=False, null=False)
    place = models.TextField(blank=False, null=False)
    authors = models.TextField(blank=False, null=False)

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def year(self) -> Optional[str]:
        return get_year_from_string(self.place)
