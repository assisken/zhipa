from django.shortcuts import render

from django.views.generic import TemplateView

class News(TemplateView):
    template_name = "index.html"
