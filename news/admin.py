from django.contrib import admin
from django.forms import Form

from .forms import NewsForm
from .models import News, NewsContentImage, NewsCover


class InlineNewsCoverAdmin(admin.TabularInline):
    model = NewsCover
    extra = 0


class InlineNewsContentImageAdmin(admin.TabularInline):
    model = NewsContentImage
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "newscover", "date", "url", "hidden", "author")
    list_display_links = ("title", "url")
    list_filter = ("hidden",)
    search_fields = ("title", "description", "text", "date", "url")
    form = NewsForm
    inlines = (
        InlineNewsCoverAdmin,
        InlineNewsContentImageAdmin,
    )
    view_on_site = True

    def save_model(self, request, obj: News, form: Form, change):
        if form.is_valid() and not obj.author:
            user = request.user
            obj.author = user
        super().save_model(request, obj, form, change)
