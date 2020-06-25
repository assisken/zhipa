import re

from django.core.exceptions import ValidationError


def validate_news_content_image_begin_name_with_a_letter(value: str):
    if not re.match(r"[^\d\s]\w*", value):
        raise ValidationError("Name must begin with a letter")
