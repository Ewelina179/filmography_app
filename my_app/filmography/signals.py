from django.contrib.auth.models import User
from .models import ActorUserRequest, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

from .get_from_imdb import actor


@receiver(post_save, sender=ActorUserRequest)
def get_from_api(sender, instance, created, **kwargs):
    if created:
        actors = actor.get_actors_ids(instance.phrase)
        instance.response = actors
        instance.save()
        print(actors)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        x = UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()