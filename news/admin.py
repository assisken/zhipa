from django.contrib import admin
from django.forms import Form

from .models import News, NewsCover, NewsContentImage
from .forms import NewsForm


class InlineNewsCoverAdmin(admin.TabularInline):
    model = NewsCover
    extra = 0


class InlineNewsContentImageAdmin(admin.TabularInline):
    model = NewsContentImage
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'hidden', 'author')
    list_display_links = ('title',)
    list_filter = ('hidden',)
    form = NewsForm
    inlines = (InlineNewsCoverAdmin, InlineNewsContentImageAdmin,)

    def save_model(self, request, obj: News, form: Form, change):
        if form.is_valid() and not obj.author:
            user = request.user
            obj.author = user
        super().save_model(request, obj, form, change)
