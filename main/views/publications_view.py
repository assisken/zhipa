from collections import defaultdict
from dataclasses import dataclass
from typing import Tuple

from django.urls import reverse
from django.views.generic import ListView

from main.models import AuthorInfo, Profile
from main.models import Publication as PublicationModel


@dataclass(frozen=True)
class Publication:
    id: int
    name: str
    place: str
    authors: Tuple[AuthorInfo, ...]


class PublicationView(ListView):
    model = PublicationModel
    template_name = "materials/publications.html"
    context_object_name = "publications"

    def get_queryset(self):
        return sorted(self.model.objects.all(), key=lambda x: x.year(), reverse=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        profiles = defaultdict(
            str,
            {
                profile.get_short_fio(): reverse(
                    "profile-publications", kwargs={"profile": profile.pk}
                )
                for profile in Profile.objects.all()
                if not profile.closed
            },
        )
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["publications"] = (
            Publication(
                id=publication.pk,
                name=publication.name,
                place=publication.place,
                authors=publication.get_authors_with_profiles(profiles),
            )
            for publication in context[self.context_object_name]
        )
        return context
