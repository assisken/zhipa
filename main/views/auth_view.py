from django.contrib.auth.views import LoginView, LogoutView


class SmiapLoginView(LoginView):
    template_name = 'auth/login.html'


class SmiapLogoutView(LogoutView):
    template_name = 'auth/logout.html'
