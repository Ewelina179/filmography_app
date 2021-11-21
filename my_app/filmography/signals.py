from .models import ActorUserRequest
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

#@receiver(post_save, sender=ActorUserRequest)
#def update_actoruserrequest(sender, instance, **kwargs):
#    pass