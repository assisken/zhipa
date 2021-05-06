from django.urls import reverse_lazy

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = reverse_lazy("accounts:login")
