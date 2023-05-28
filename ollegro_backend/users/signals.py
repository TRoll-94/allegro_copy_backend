from django.db.models.signals import post_save
from django.dispatch import receiver

from users.consts import DefaultUserTypes
from users.models import User, UserType


@receiver(post_save, sender=User)
def update_user(sender, instance: User, created, **kwargs):
    """ Set default values """
    if instance.user_type is None:
        user_type = UserType.objects.filter(code=DefaultUserTypes.customer.value()).first()
        if user_type is None:
            return
        instance.user_type = user_type
        instance.save()
