from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import View

from main.models import File


class LinkView(View):
    def get(self, request, link: str):
        file = File.objects.get(link=link)
        if not file.file:
            raise Http404()
        return redirect(file.file.url)
