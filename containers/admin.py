from typing import List, Optional

from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest

from .models import Container


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = [
        "name",
        "group",
        "do_not_remove",
        "cores",
        "memory_gb",
        "partition_size_gb",
    ]
    readonly_fields = ["name"]
    list_filter = ["do_not_remove"]

    def get_readonly_fields(
        self, request: HttpRequest, obj: Optional[Model] = None
    ) -> List[str]:
        if obj is None:
            return self.readonly_fields
        return self.readonly_fields + ["partition_size_gb"]
