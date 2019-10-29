import re

from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.contrib.admin.forms import forms as admin_forms
from django.core.exceptions import ValidationError

from main.models import Group, Teacher, News
from utils.news_md_to_html import NewsLexer


def check_items(value: str):
    items = value.split('\n')
    for line, item in enumerate(items):
        item = item.replace(' 	', '||')
        if item.count('||') != 2:
            count = item.count("||") + 1
            raise ValidationError(f'Required 3 or more items, got {count} on line {line + 1}')


class SeveralPublicationsForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    couple_items = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_items,)
    )


def check_schedule(value: str):
    items = value.split('\n')
    for line, item in enumerate(items):
        if item.count('||') != 4:
            count = item.count("||") + 1
            raise ValidationError(f'Required 5 or more items, got {count} on line {line + 1}')


class ExtramuralScheduleForm(admin_forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    group = admin_forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(study_form=Group.EXTRAMURAL).order_by('semester', 'name'),
        required=True,
        widget=admin_widgets.FilteredSelectMultiple(
            verbose_name=Group._meta.verbose_name,
            is_stacked=False
        )
    )
    schedule = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_schedule,)
    )


class GetGroupScheduleForm(admin_forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    groups = admin_forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by('-study_form', 'degree', 'semester', 'name'),
        required=True,
    )
    from_week = admin_forms.IntegerField(min_value=1, max_value=17)


class GetTeacherScheduleForm(admin_forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    groups = admin_forms.ModelMultipleChoiceField(
        queryset=Teacher.objects.all(),
        required=True,
        widget=admin_widgets.FilteredSelectMultiple(
            verbose_name=Teacher._meta.verbose_name,
            is_stacked=False
        )
    )


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ('author',)

    def clean(self):
        images = frozenset(v for k, v in self.data.items() if v and re.match(r'newscontentimage_set-\d+-name', k))
        value: str = self.data['text']
        for line in value.splitlines():
            match = NewsLexer.several_images.match(line)
            if not match:
                continue
            _, _, text_images = NewsLexer.get_items(match)
            if not frozenset(text_images) <= images:
                raise ValidationError({'text': 'Text contains image that does not exist'})
            return super().clean()
