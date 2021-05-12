from django.db.models import signals
from django.dispatch import receiver

from main.models import User
from main.utils.unify import unify_fio


@receiver(signals.post_save, sender=User)
def unify_names(sender: User, instance: User, **kwargs):

