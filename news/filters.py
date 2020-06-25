from django.conf import settings

from .models import NewsContentImage
from .news_md_to_html import MD

DEFAULT_IMG = getattr(settings, "DEFAULT_IMG", "default.png")


def markdown_to_html(text: str):
    return MD(text)


def news_text_to_html(text: str, news_id: int):
    content = markdown_to_html(text)
    attachments = NewsContentImage.objects.filter(news_id=news_id)

    replacing_images = {}
    for a in attachments:
        replacing_images[a.name] = a.img.url if a.img else DEFAULT_IMG

    content = content.format(**replacing_images)
    return content
