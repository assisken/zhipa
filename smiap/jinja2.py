from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import date
from django.urls import reverse
from jinja2 import Environment

from news.filters import markdown_to_html, news_text_to_html


def environment(**options):
    extensions = [] if 'extensions' not in options else options['extensions']
    extensions += [
        'sass_processor.jinja2.ext.SassSrc',
        'compressor.contrib.jinja2ext.CompressorExtension',
    ]
    options['extensions'] = extensions

    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.filters.update({
        'date': date,
        'markdown': markdown_to_html,
        'news_text': news_text_to_html,
        'no_break_space': lambda text: text.replace(' ', ' '),
    })
    return env
