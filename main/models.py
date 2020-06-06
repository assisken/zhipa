import os
import uuid
from datetime import datetime
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models

from main.utils.date import get_year_from_string


class User(AbstractUser):
    pass


def get_files_path(instance: 'File', filename: str):
    _uuid = uuid.uuid4()
    return os.path.join('files', str(_uuid), filename)


def get_random_link():
    return str(uuid.uuid4())[:8]


class File(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=200, unique=True, null=False, blank=False, default=get_random_link)
    file = models.FileField(upload_to=get_files_path, max_length=200, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    uploaded_date = models.DateTimeField(null=False, blank=False, auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        super().delete()
        if self.file:
            os.remove(self.file.path)
            os.removedirs(os.path.dirname(self.file.path))


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
