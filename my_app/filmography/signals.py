from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Actor, ActorUserRequest, Movie, UserProfile
from django.apps import apps

from .get_from_imdb import ActorInfo

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        x = UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=Actor)
def get_movies_from_api(sender, instance, created, **kwargs):
    if created:
        movies = apps.get_model("filmography.MovieRequest").objects.create(actor_imdb_id=instance.imdb_id)


@receiver(post_save, sender=ActorUserRequest) # chyba powinno być jak zmienia status?
def change_daily_api_counter(sender, instance, created, **kwargs):
    if created:
        pass
        #print(instance.phrase)
        #print(instance.status)
        #print(instance.user) # tutaj pusto (?)
        #print(apps.get_model('filmography.UserProfile').objects.filter(user=instance.user.userprofile))
