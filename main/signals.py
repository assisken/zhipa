from django.contrib.flatpages.models import FlatPage
from django.db.models import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from main.urls import urlpatterns


@receiver(pre_delete, sender=FlatPage)
def delete_is_available_returned(sender: FlatPage, instance: FlatPage, **kwargs):
    url = instance.url[1:] if instance.url.startswith('/') else instance.url
    if any(url == str(urlpattern.pattern) for urlpattern in urlpatterns):
        raise ProtectedError('This page cannot be deleted', instance)
