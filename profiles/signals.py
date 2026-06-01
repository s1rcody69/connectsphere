from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile when a new User is registered.
    The 'created' parameter is True only when the User is first created,
    not when it is updated. This prevents duplicate profiles.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the Profile whenever the User is saved.
    This keeps the profile in sync with the user.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()