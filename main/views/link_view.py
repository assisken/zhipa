from django.shortcuts import redirect
from django.views.generic import View

from main.models import File


class LinkView(View):
    def get(self, request, link: str):
        file = File.objects.get(link=link)
        return redirect(file.file.url)
