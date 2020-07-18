import os

from django.contrib.staticfiles.storage import staticfiles_storage

from smiap.settings import BASE_DIR

print("running test environment")

LOCALE = "ru_RU.UTF-8"
LANG = LOCALE
LANGUAGE = "en_US:en"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_NAME": ":memory:",
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

FILES_ROOT = "/static"
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
