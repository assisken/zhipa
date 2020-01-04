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


DATE_FORMAT = r'^(?P<day>\d\d)\.(?P<month>\d\d)\.?(?P<year>\d\d\d\d)?$'
TIME_FORMAT = r'^(\d\d):(\d\d)$'
TEACHER_FORMAT = r'^[А-Яа-яЁё]+ [А-Яа-яЁё]\.[А-Яа-яЁё]\.(, [А-Яа-яёЁ]+ [А-Яа-яЁё]\.[А-Яа-яЁё]\.)*$'
PLACE_FORMAT = r'^(?P<cabinet>[\S]+) ?(?P<area>.*)$'


def check_columns_count(value: str):
    count = 5
    items = value.split('\n')
    for line, item in enumerate(items):
        col_count = item.count('||') + 1
        if col_count != count:
            raise ValidationError(f'Требуется {count} столбцов, но было получено {col_count} столбцов.\n'
                                  f'Строка: {line + 1}')


def parse_columns(func):
    def wrapper(value: str):
        pattern = re.compile(r'(?P<date>.*)\|\|(?P<time>.*)\|\|(?P<item>.*)\|\|(?P<teacher>.*)\|\|(?P<place>.*)')
        kwargs = {
            'dates': (x.group('date').strip() for x in pattern.finditer(value)),
            'times': (x.group('time').strip() for x in pattern.finditer(value)),
            'items': (x.group('item').strip() for x in pattern.finditer(value)),
            'teachers': (x.group('teacher').strip() for x in pattern.finditer(value)),
            'places': (x.group('place').strip() for x in pattern.finditer(value)),
        }

        return func(**kwargs)

    return wrapper


@parse_columns
def check_format_date(dates, **kwargs):
    for line, date in enumerate(dates):
        if not re.match(DATE_FORMAT, date) and date != '':
            raise ValidationError('Дата должна быть оформлена в формате БDD.MM" или "DD.MM.YYYY".\n'
                                  'Ставить пустымв случае, если желаемое значение было "По договору с преподавателем"\n'
                                  f'Строка {line + 1}, значение: "{date}"')


@parse_columns
def check_time_format(times, **kwargs):
    for line, time in enumerate(times):
        if not re.match(TIME_FORMAT, time) and time != '':
            raise ValidationError('Время должно быть оформлено в формате "HH:MM".\n'
                                  'Также возможно опустить данный столбец (оставить пустым)\n'
                                  f'Строка {line + 1}, значение: "{time}"')


@parse_columns
def check_teacher_abbreviation_format(teachers, **kwargs):
    for line, teacher in enumerate(teachers):
        if not re.match(TEACHER_FORMAT, teacher) and teacher != '':
            raise ValidationError('Преподаватель должен быть оформлен в формате "Фамилия И.О." Например: Иванов И.И.\n'
                                  'Возможно перечисление преподавателей, которое нужно оформить в формате '
                                  '"Фамилия1 И.О., Фамилия2 И.О., ...". Например:\n'
                                  'Иванов И.И., Петров П.П., Семёнов С.С.\n'
                                  'Также возможно опустить данный столбец (оставить пустым)\n'
                                  f'Строка {line + 1}, значение: "{teacher}"')


@parse_columns
def check_place_abbreviation_format(places, **kwargs):
    for line, place in enumerate(places):
        if not re.match(PLACE_FORMAT, place) and place != '':
            raise ValidationError('Информация о месте проведения занятия должна быть в формате "Кабинет Площадка" '
                                  'или "Место". Например:\n'
                                  '507В Орш.\n'
                                  'стадион\n'
                                  'Б-448 ГУК\n'
                                  'Также возможно опустить данный столбец (оставить пустым)\n'
                                  f'Строка {line + 1}, значение: "{place}"')


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
    separator = forms.CharField(
        initial='||',
        disabled=True
    )
    schedule = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'vLargeTextField'}),
        validators=(
            check_columns_count,
            check_format_date,
            check_time_format,
            check_teacher_abbreviation_format,
            check_place_abbreviation_format,
        )
    )

    def schedule_fields(self):
        data = self.cleaned_data['schedule']
        separator = self.cleaned_data['separator']
        for line in data.splitlines():
            date, time, item, teachers, place = line.split(separator, maxsplit=4)
            date = date.strip()
            time = time.strip()
            item = item.strip()
            _teachers = tuple(teacher.strip() for teacher in teachers.split(', '))
            place = place.strip()

            if date == '':
                date = None
            if time == '':
                time = None
            if item == '':
                item = None
            if _teachers == ('',):
                _teachers = None
            if place == '':
                place = None
            yield date, time, item, _teachers, place


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
