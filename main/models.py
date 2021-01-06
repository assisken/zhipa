import os
import re
import uuid
from collections import namedtuple
from typing import Dict, List, Optional, Tuple

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from transliterate import translit

from main.utils.date import get_year_from_string
from main.utils.unify import unify_fio
from schedule.models import Group


class User(AbstractUser):
    pass


def get_files_path(instance: "File", filename: str):
    _uuid = uuid.uuid4()
    return os.path.join("files", str(_uuid), filename)


def get_random_link():
    return str(uuid.uuid4())[:8]


class File(models.Model):
    name = models.CharField(max_length=200)
    link = models.CharField(
        max_length=200, unique=True, null=False, blank=False, default=get_random_link
    )
    file = models.FileField(
        upload_to=get_files_path, max_length=200, null=True, blank=True
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    uploaded_date = models.DateTimeField(null=False, blank=False, auto_now=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        super().delete()
        if self.file:
            os.remove(self.file.path)
            os.removedirs(os.path.dirname(self.file.path))

    def get_absolute_url(self):
        return reverse("short-file", kwargs={"link": self.link})


def get_profile_image_path(instance: "Profile", filename: str):
    return os.path.join("profile", str(instance.pk), filename)


class ProfileManager(models.Manager):
    def filter_by_fio(self, fio: str):
        lastname, abbreviation, *_ = unify_fio(fio).split(" ")
        firstname_beg, middlename_beg, *_ = abbreviation.split(".")
        return (
            super()
            .get_queryset()
            .filter(
                lastname=lastname,
                firstname__startswith=firstname_beg,
                middlename__startswith=middlename_beg,
            )
        )


class Profile(models.Model):
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30)
    img = models.ImageField(
        max_length=60,
        null=True,
        default=None,
        upload_to=get_profile_image_path,
        blank=True,
    )
    closed = models.BooleanField(
        default=True,
        verbose_name="Закрытый профиль",
        help_text="Снимите галочку, чтобы открыть профиль",
    )

    objects = ProfileManager()

    def __str__(self):
        return self.get_fio()

    def get_absolute_url(self):
        return reverse("profile-description", kwargs={"profile": self.id})

    def get_fio(self):
        return f"{self.lastname} {self.firstname} {self.middlename}"

    def get_short_fio(self):
        return f"{self.lastname} {self.firstname[0]}.{self.middlename[0]}."

    def get_kebab_fio(self):
        trans = translit(self.get_fio(), "ru", reversed=True).replace(" ", "")
        return re.sub(r"(?<!^)(?=[A-Z])", "-", trans).lower()


class Staff(Profile):
    regalia = models.CharField(max_length=60)
    description = models.TextField(null=False, default="", blank=True)
    leader = models.BooleanField(default=False)
    lecturer = models.BooleanField(default=True)
    hide = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Staff"
        ordering = (
            "-leader",
            "-lecturer",
            "hide",
            "lastname",
            "firstname",
            "middlename",
            "pk",
        )

    def get_profile_url(self):
        return super().get_absolute_url()

    def get_absolute_url(self):
        return reverse("staff") + f"#{self.get_kebab_fio()}"


class Student(Profile):
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)


AuthorInfo = namedtuple("AuthorInfo", "fio link")


class Publication(models.Model):
    name = models.TextField(blank=False, null=False)
    place = models.TextField(blank=False, null=False)
    authors = models.TextField(blank=False, null=False)

    author_profiles = models.ManyToManyField(
        Profile,
        blank=True,
        editable=False,
        help_text="При создании новой публикации заполняется автоматически.",
    )

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publications") + f"#{self.id}"

    def year(self) -> Optional[str]:
        return get_year_from_string(self.place)

    def get_author_profiles(self) -> List[Profile]:
        authors = re.split(r", +", self.authors)
        return [
            profile for fio in authors for profile in Profile.objects.filter_by_fio(fio)
        ]

    def get_authors_with_profiles(
        self, profiles: Dict[str, str]
    ) -> Tuple[AuthorInfo, ...]:
        authors = re.split(r", +", self.authors)
        return tuple(AuthorInfo(fio=fio, link=profiles[fio]) for fio in authors)
