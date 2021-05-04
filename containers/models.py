from django.core.validators import MaxValueValidator as Max
from django.core.validators import MinValueValidator as Min
from django.db import models

from .utils import normalize_group_name


class Container(models.Model):
    name = models.CharField(
        verbose_name="Container name",
        editable=False,
        max_length=100,
        null=False,
        blank=False,
        unique=True,
    )
    group = models.OneToOneField("schedule.Group", on_delete=models.SET_NULL, null=True)
    do_not_remove = models.BooleanField(default=False, null=False, blank=False)

    cores = models.IntegerField(
        validators=[Min(1), Max(100)], null=False, blank=False, default=1
    )
    memory_gb = models.IntegerField(
        validators=[Min(1), Max(1000)],
        null=False,
        blank=False,
        default=2,
        verbose_name="Memory in GB",
    )
    partition_size_gb = models.IntegerField(
        validators=[Min(1), Max(1000)],
        null=False,
        blank=False,
        default=10,
        verbose_name="Partition size in GB",
        help_text="Affects only when creating a container",
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.group is not None:
            self.name = normalize_group_name(self.group.name)
        super().save(force_insert, force_update, using, update_fields)
