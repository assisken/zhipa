import re

from django import forms
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from djangoeditorwidgets.widgets import MonacoEditorWidget

from .models import News
from .news_md_to_html import NewsLexer


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget = MonacoEditorWidget(
            attrs={"data-language": "markdown", "data-wordwrap": "on"}
        )
        self.fields["text"].help_text = render_to_string(
            "layout/markdown_introduction.html"
        )
        self.fields["text"].widget = MonacoEditorWidget(
            attrs={"data-language": "markdown", "data-wordwrap": "on"}
        )

    class Meta:
        model = News
        fields = "__all__"
        exclude = (
            "author",
            "cover",
        )

    def clean(self):
        self.check_text_has_image_name_in_form()
        return super().clean()

    def check_text_has_image_name_in_form(self):
        images = frozenset(
            v
            for k, v in self.data.items()
            if v and re.match(r"newscontentimage_set-\d+-name", k)
        )
        value: str = self.data["text"]
        for line in value.splitlines():
            match = NewsLexer.several_images.match(line)
            if not match:
                continue
            _, _, text_images = NewsLexer.get_items(match)
            if not frozenset(text_images) <= images:
                raise ValidationError(
                    {"text": "Text contains image that does not exist"}
                )
