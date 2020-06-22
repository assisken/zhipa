from split_settings.tools import include

from smiap.settings.components.general import REST_FRAMEWORK

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '10.8.0.0/24',
    'duck.nepnep.ru',
    'vl4dmati.mati.su'
]
HTML_MINIFY = False
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

development_components = [
    '../components/debug_toolbar.py',
]

include(*development_components)
