import os

ALLOWED_HOSTS = [
    "*",
]
HTML_MINIFY = True
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
SASS_OUTPUT_STYLE = "compressed"

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
