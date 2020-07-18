import os

from django.contrib.staticfiles.storage import staticfiles_storage
from split_settings.tools import include

from smiap.settings.components.general import BASE_DIR, REST_FRAMEWORK

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "10.8.0.0/24",
    "duck.nepnep.ru",
    "vl4dmati.mati.su",
]
HTML_MINIFY = False
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False
SASS_OUTPUT_STYLE = "expanded"

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    *REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"],
    "rest_framework.renderers.BrowsableAPIRenderer",
]

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "TEST": {"NAME": "test_smiap"},
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

FILES_ROOT = "/tmp/static"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(FILES_ROOT, "static")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(FILES_ROOT, "media")
FILE_UPLOAD_PERMISSIONS = 0o644
DEFAULT_IMG = staticfiles_storage.url("default.png")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    MEDIA_ROOT,
)
SASS_PROCESSOR_ROOT = os.path.join(STATIC_ROOT, "stylesheets")

development_components = [
    "../components/debug_toolbar.py",
]

include(*development_components)
