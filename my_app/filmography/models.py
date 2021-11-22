from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    objects = models.Manager()

class ActorUser(models.Model):
    user = models.ForeignKey('filmography.UserProfile', on_delete=models.CASCADE)
    actor = models.ForeignKey('filmography.Actor', on_delete=models.CASCADE)


class Actor(models.Model):
    fullname = models.CharField(max_length=128)


class Movie(models.Model):
    id_from_imdb = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128)


class ActorMovie(models.Model):
    actor = models.ForeignKey('filmography.Actor', on_delete=models.CASCADE)
    movie = models.ForeignKey('filmography.Movie', on_delete=models.CASCADE)


class ActorUserRequest(models.Model):
    user = models.ForeignKey('filmography.UserProfile', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    phrase = models.CharField(max_length=64)
    response = models.TextField(blank=True, default="")
