from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Actor, ActorUserRequest, MovieRequest, UserProfile
from .forms import ActorUserRequestForm
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

@receiver(post_save, sender=ActorUserRequest)
def get_actors_from_api(sender, instance, created, **kwargs):
    if created:
        actouserrequest = apps.get_model("filmography.ActorUserRequest").set_response(instance)

@receiver(post_save, sender=MovieRequest)
def get_actors_from_api(sender, instance, created, **kwargs):
    if created:
        movierequest = apps.get_model("filmography.MovieRequest").set_response(instance)

@receiver(post_save, sender=ActorUserRequest)
def change_daily_api_counter(sender, instance, created, **kwargs):
    if created:
        pass