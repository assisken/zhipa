from .history import History
from django.views.generic import TemplateView


class News(TemplateView):
    template_name = "index.html"
