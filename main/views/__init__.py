from .history import History
from .staff import StaffView
from django.views.generic import TemplateView


class News(TemplateView):
    template_name = "index.html"
