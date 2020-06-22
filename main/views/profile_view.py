from django.http import Http404
from django.views.generic import DetailView

from main.models import Staff, Publication as PublicationModel, Profile
from main.views import PublicationView


class ProfileDescriptionView(DetailView):
    model = Staff
    template_name = 'profile/description.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'profile'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.closed:
            raise Http404()
        return super().get(request, *args, **kwargs)


class ProfilePublicationsView(PublicationView):
    model = PublicationModel
    context_object_name = 'publications'
    template_name = 'profile/publications.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['profile'] = self.profile
        return context

    def get_queryset(self):
        return sorted(
            self.model.objects.filter(author_profiles__exact=self.kwargs['profile']),
            key=lambda x: x.year(),
            reverse=True
        )

    def get(self, request, *args, **kwargs):
        self.profile = Profile.objects.get(pk=self.kwargs['profile'])
        if self.profile.closed:
            raise Http404()
        return super().get(request, *args, **kwargs)
