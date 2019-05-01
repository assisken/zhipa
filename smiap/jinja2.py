from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaultfilters import date
from django.urls import reverse
from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.filters['date'] = date
    return env
