from django.contrib.flatpages.models import FlatPage
from django.db.models import ProtectedError
from django.db.models import signals
from django.dispatch import receiver

from main.urls import urlpatterns
from main.models import Profile, Publication
from main.utils.unify import unify_fio


@receiver(signals.pre_delete, sender=FlatPage)
def delete_is_available_returned(sender: FlatPage, instance: FlatPage, **kwargs):
    url = instance.url[1:] if instance.url.startswith('/') else instance.url
    if any(url == str(urlpattern.pattern) for urlpattern in urlpatterns):
        raise ProtectedError('This page cannot be deleted', instance)


@receiver(signals.pre_save, sender=Profile)
def unify_names(sender: Profile, instance: Profile, **kwargs):
    instance.lastname = unify_fio(instance.lastname)
    instance.firstname = unify_fio(instance.firstname)
    instance.middlename = unify_fio(instance.middlename)


@receiver(signals.post_save, sender=Publication)
def add_links_to_author_profiles(sender: Publication, instance: Publication, **kwargs):
    instance.author_profiles.set(instance.get_author_profiles())
