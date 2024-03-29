from django.contrib import admin
from django.db.models import QuerySet
from django.urls import path

from main.types import Degree

from .admin_views import (
    AddExtramuralSchedule,
    GetGroupExtramuralScheduleXlsxView,
    GetGroupFulltimeScheduleXlsxView,
    GetTeacherSchedule,
)
from .models import ExtramuralSchedule, FullTimeSchedule, Group, Teacher


class GroupCourseFilter(admin.SimpleListFilter):
    title = "Course"
    parameter_name = "courses"

    def lookups(self, request, model_admin):
        courses = Group.objects.distinct("degree", "course").only("course")
        return sorted({(c.course, f"{c.course} курс") for c in courses})

    def queryset(self, request, queryset: QuerySet):
        course = self.value()
        if course:
            return queryset.filter(
                semester__gte=int(course) * 2 - 1, semester__lte=int(course) * 2
            )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        "name",
        "study_form",
        "get_degree",
        "semester",
        "course",
    )
    list_filter = ("study_form", GroupCourseFilter)

    def get_degree(self, obj: Group):
        return Degree(obj.degree).name.casefold().capitalize()

    get_degree.short_description = "Degree"  # type: ignore
    get_degree.admin_order_field = "degree"  # type: ignore


class TeacherIsStuffFilter(admin.SimpleListFilter):
    title = "Teacher is staff"
    parameter_name = "is_staff"

    def lookups(self, request, model_admin):
        return ("Y", "Yes"), ("N", "No")

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            value = self.value() == "Y"
            return queryset.filter(staff__isnull=not value)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("__str__", "staff")
    list_filter = (TeacherIsStuffFilter,)


class ItemInline(admin.TabularInline):
    model = FullTimeSchedule
    extra = 1


class FullTimeGroupFilter(admin.SimpleListFilter):
    title = "Groups"
    parameter_name = "group"
    study_form = Group.FULL_TIME

    def lookups(self, request, model_admin):
        groups = Group.objects.filter(study_form=self.study_form)
        return ((group.name, group.name) for group in groups)

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            return queryset.filter(group__name=self.value())


@admin.register(FullTimeSchedule)
class FullTimeScheduleAdmin(admin.ModelAdmin):
    change_list_template = "admin/schedule/list.html"
    ordering = ("date", "time")
    list_display = (
        "date",
        "week",
        "time",
        "item_type",
        "schedule_type",
        "group",
        "name",
        "place",
        "hidden",
    )
    list_filter = (
        FullTimeGroupFilter,
        "item_type",
        "schedule_type",
        "hidden",
        "time",
        "date",
        "place",
    )
    filter_horizontal = ("teachers",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "get-group-schedule/",
                GetGroupFulltimeScheduleXlsxView.as_view(schedule=FullTimeSchedule),
            ),
            path(
                "get-teacher-schedule/",
                GetTeacherSchedule.as_view(schedule=FullTimeSchedule),
            ),
        ]
        return my_urls + urls


class ExtramuralGroupFilter(FullTimeGroupFilter):
    study_form = Group.EXTRAMURAL


@admin.register(ExtramuralSchedule)
class ExtramuralScheduleAdmin(admin.ModelAdmin):
    change_list_template = "admin/extramural_schedule/list.html"
    ordering = ("date",)
    list_display = ("name", "date", "schedule_type", "group")
    list_filter = (ExtramuralGroupFilter, "schedule_type")
    filter_horizontal = FullTimeScheduleAdmin.filter_horizontal

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "add-extramural/",
                AddExtramuralSchedule.as_view(),
                name="admin-add-several-extramural",
            ),
            path(
                "get-group-schedule/",
                GetGroupExtramuralScheduleXlsxView.as_view(schedule=ExtramuralSchedule),
            ),
            path(
                "get-teacher-schedule/",
                GetTeacherSchedule.as_view(schedule=ExtramuralSchedule),
            ),
        ]
        return my_urls + urls
