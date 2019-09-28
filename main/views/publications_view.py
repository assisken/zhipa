from django.views.generic import ListView

from main.models import Publication


class PublicationView(ListView):
    model = Publication
    template_name = 'materials/publications.html'
    context_object_name = 'publications'
