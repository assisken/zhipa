from django.views.generic import ListView

from main.models import Publication


class PublicationView(ListView):
    model = Publication
    template_name = 'materials/publications.html'
    context_object_name = 'publications'

    def get_queryset(self):
        return sorted(self.model.objects.all(), key=lambda x: x.year(), reverse=True)
