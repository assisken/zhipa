import re

from django import forms
from django.contrib.admin import widgets as admin_widgets
from django.core.exceptions import ValidationError
from django_registration.forms import RegistrationFormUniqueEmail

from main.models import Group, Teacher, News, User, ExtramuralSchedule
from utils.news_md_to_html import NewsLexer


def check_items(value: str):
    items = value.split('\n')
    for line, item in enumerate(items):
        item = item.replace(' 	', '||')
        if item.count('||') != 2:
            count = item.count("||") + 1
            raise ValidationError(f'Required 3 or more items, got {count} on line {line + 1}')


class SmiapRegistrationForm(RegistrationFormUniqueEmail):
    error_css_class = 'errors'
    required_css_class = 'required'

    class Meta:
        model = User
        fields = ("email", "username",)


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


class ExtramuralScheduleForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'

    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(study_form=Group.EXTRAMURAL),
        required=True,
        widget=admin_widgets.FilteredSelectMultiple(
            verbose_name=Group._meta.verbose_name,
            is_stacked=False
        )
    )
    schedule_type = forms.ChoiceField(
        choices=ExtramuralSchedule.SCHEDULE_TYPES
    )
    schedule = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(check_schedule,)
    )


class GetGroupScheduleForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.order_by('-study_form', 'degree', 'semester', 'name'),
        required=True,
    )
    from_week = forms.IntegerField(min_value=1, max_value=17)


class GetTeacherScheduleForm(forms.Form):
    error_css_class = 'errors'
    required_css_class = 'required'
    groups = forms.ModelMultipleChoiceField(
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
        self.check_text_has_image_name_in_form()
        return super().clean()

    def check_text_has_image_name_in_form(self):
        images = frozenset(v for k, v in self.data.items() if v and re.match(r'newscontentimage_set-\d+-name', k))
        value: str = self.data['text']
        for line in value.splitlines():
            match = NewsLexer.several_images.match(line)
            if not match:
                continue
            _, _, text_images = NewsLexer.get_items(match)
            if not frozenset(text_images) <= images:
                raise ValidationError({'text': 'Text contains image that does not exist'})
