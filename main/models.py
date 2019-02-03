import os

from django.db import models
from django.db.models import F

def get_image_path():
    return os.path.join('images', 'lecturers')


class Staff(models.Model):
    lastname = models.CharField(max_length=30, null=False)
    firstname = models.CharField(max_length=30, null=False)
    middlename = models.CharField(max_length=30, null=False)
    img = models.ImageField(max_length=60, null=True, default=None, upload_to=get_image_path(), blank=True)
    regalia = models.CharField(max_length=60, null=False)
    description = models.TextField(null=True, default=None, blank=True)
    leader = models.BooleanField(null=False, default=False)
    lecturer = models.BooleanField(null=False, default=True)
    hide = models.BooleanField(null=False, default=True)

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
