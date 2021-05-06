from typing import Optional

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.models import FlatPage
from django.db.models import QuerySet
from django.db.models.deletion import ProtectedError
from django.forms import Form
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from main.forms import FlatpageForm
from main.models import File, Profile, Publication, Staff, Student, User
from main.urls import urlpatterns
from main.utils.date import get_year_from_string
from main.views.admin.couple_publications import SeveralPublicationsView


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("__str__", "regalia", "leader", "lecturer", "hide")
    list_filter = ("leader", "lecturer", "hide")
    search_fields = ("lastname", "firstname", "middlename", "regalia")


@admin.register(User)
class SmiapUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "closed")
    list_display_links = ("__str__",)
    ordering = ("lastname", "firstname", "middlename")
    search_fields = ("lastname", "firstname", "middlename")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


class PublicationYearFilter(admin.SimpleListFilter):
    title = "Publication Year"
    parameter_name = "publication"

    def lookups(self, request, model_admin):
        def get_year():
            for pub in Publication.objects.values("place"):
                year = get_year_from_string(pub["place"])
                if year is None:
                    yield "Не определен"
                    continue
                yield year

        years = frozenset(get_year())
        return ((year, year) for year in sorted(years))

    def queryset(self, request, queryset: QuerySet):
        if self.value():
            return queryset.filter(place__contains=self.value())


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    change_list_template = "admin/publications/list.html"
    list_display = ("id", "year", "name", "place", "authors")
    list_display_links = ("name",)
    list_filter = (PublicationYearFilter,)
    search_fields = ("id", "name", "place", "authors")
    readonly_fields = ("author_profiles",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("add-couple/", SeveralPublicationsView.as_view())]
        return my_urls + urls


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_link", "file", "uploaded_date", "author")
    ordering = ("-uploaded_date",)
    exclude = ("author", "uploaded_date")
    list_display_links = ("name",)

    def get_link(self, obj: File):
        return mark_safe(
            f'<a href="{reverse("short-file", kwargs={"link": obj.link})}">{obj.link}</a>'
        )

    get_link.short_description = "Link"  # type: ignore

    def save_model(self, request, obj: File, form: Form, change):
        if form.is_valid() and not obj.author:
            user = request.user
            obj.author = user
        super().save_model(request, obj, form, change)


admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageAdmin(FlatPageAdminOld):
    delete_error_msg = "You cannot delete this page: {page}"
    form = FlatpageForm

    def has_delete_permission(self, request, obj: Optional[FlatPage] = None):
        if obj:
            url = obj.url[1:] if obj.url.startswith("/") else obj.url
            return all(url != str(urlpattern.pattern) for urlpattern in urlpatterns)
        return super().has_delete_permission(request, obj)

    def delete_view(self, request, object_id, extra_context=None):
        try:
            return super().delete_view(request, object_id, extra_context)
        except ProtectedError as e:
            msg = self.delete_error_msg.format(page=e.protected_objects)
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse(
                "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                args=(object_id,),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(return_url)

    def response_action(self, request, queryset):
        try:
            return super().response_action(request, queryset)
        except ProtectedError as e:
            msg = self.delete_error_msg.format(page=e.protected_objects)
            self.message_user(request, msg, messages.ERROR)
            opts = self.model._meta
            return_url = reverse(
                "admin:%s_%s_changelist" % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(return_url)


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        BaseUserAdmin.fieldsets[:1]
        + (
            (
                _("Personal info"),
                {"fields": ("last_name", "first_name", "middle_name", "email")},
            ),
            ("Профиль", {"fields": ("profile",)}),
        )
        + BaseUserAdmin.fieldsets[2:]
    )
