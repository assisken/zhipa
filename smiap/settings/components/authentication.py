from django.urls import reverse_lazy

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = reverse_lazy("accounts:login")

# Mail settings for django-registration
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'no-reply@smiap.ru'
