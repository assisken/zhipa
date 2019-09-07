from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet

from main.models import *
from main.types import Degree
from utils.group import degree


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'regalia', 'leader', 'lecturer', 'hide')
    list_filter = ('leader', 'lecturer', 'hide')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'hidden')
    list_display_links = ('title',)
    list_filter = ('hidden',)


class GroupCourseFilter(admin.SimpleListFilter):
    title = 'Course'
    parameter_name = 'courses'

    def lookups(self, request, model_admin):
        courses = Group.objects.distinct('course').only('course')
        return ((c.course, f'{c.course} курс') for c in courses)

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            value = int(self.value())
            return queryset.filter(semester__gte=value * 2 - 1,
                                   semester__lte=value * 2)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    ordering = ('degree', 'course', '-study_form', 'name')
    list_display = ('name', 'study_form', 'get_degree', 'semester', 'course')
    list_filter = ('study_form', GroupCourseFilter)

    def get_degree(self, obj: Group):
        return Degree(obj.degree).name.casefold().capitalize()

    get_degree.short_description = 'Degree'
    get_degree.admin_order_field = 'degree'


@admin.register(User)
class SmiapUserAdmin(UserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'staff')


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'week', 'group')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('day', 'starts_at', 'ends_at', 'type', 'name')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass
