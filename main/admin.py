from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.forms import Form
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from main.models import *
from main.views.admin.couple_publications import SeveralPublicationsView


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'regalia', 'leader', 'lecturer', 'hide')
    list_filter = ('leader', 'lecturer', 'hide')


@admin.register(User)
class SmiapUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


class PublicationYearFilter(admin.SimpleListFilter):
    title = 'Publication Year'
    parameter_name = 'publication'

    def lookups(self, request, model_admin):
        def get_year():
            for pub in Publication.objects.values('place'):
                year = get_year_from_string(pub['place'])
                if year is None:
                    yield 'Не определен'
                    continue
                yield year
        years = frozenset(get_year())
        return ((year, year) for year in sorted(years))

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            return queryset.filter(place__contains=self.value())


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    change_list_template = 'admin/publications/list.html'
    list_display = ('id', 'year', 'name', 'place', 'authors')
    list_display_links = ('name',)
    list_filter = (PublicationYearFilter,)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add-couple/', SeveralPublicationsView.as_view())
        ]
        return my_urls + urls


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_link', 'file', 'uploaded_date', 'author')
    ordering = ('-uploaded_date',)
    exclude = ('author', 'uploaded_date')
    list_display_links = ('name',)

    def get_link(self, obj: File):
        return mark_safe(f'<a href="{reverse("short-file", kwargs={"link": obj.link})}">{obj.link}</a>')

    get_link.short_description = 'Link'

    def save_model(self, request, obj: File, form: Form, change):
        if form.is_valid() and not obj.author:
            user = request.user
            obj.author = user
        super().save_model(request, obj, form, change)
