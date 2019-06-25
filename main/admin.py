from django.contrib import admin
from django.db.models import QuerySet

from main.models import Staff, News, Group
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
        courses = {i.course() for i in Group.objects.all()}
        return ((c, f'{c} курс') for c in courses)

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            value = int(self.value())
            return queryset.filter(semester__gte=value * 2 - 1,
                                   semester__lte=value * 2)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'study_form', 'get_degree', 'semester', 'get_course')
    list_filter = ('study_form', GroupCourseFilter)

    def get_course(self, obj: Group):
        return obj.course()

    def get_degree(self, obj: Group):
        return degree(obj.name).name.casefold().capitalize()

    get_course.short_description = 'Course'
    get_degree.short_description = 'Degree'
    get_course.admin_order_field = 'semester'
