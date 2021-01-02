from django.contrib.auth.backends import ModelBackend


class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if request:
            request.user = user
        return user
