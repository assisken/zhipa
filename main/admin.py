from django.contrib import admin
from django.db.models import QuerySet

from main.models import Staff, News, Group


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'regalia', 'leader', 'lecturer', 'hide')
    list_filter = ('leader', 'lecturer', 'hide')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'hidden')
    list_display_links = ('title',)
    list_filter = ('hidden',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_course')

    def get_course(self, obj: Group):
        return obj.course()

    get_course.short_description = 'Course'
