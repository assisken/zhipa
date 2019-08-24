from django.contrib.auth import get_user_model, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse


class SmiapLoginView(LoginView):
    template_name = 'auth/login.html'
    # redirect_authenticated_user = True


class SmiapLogoutView(LogoutView):
    pass
