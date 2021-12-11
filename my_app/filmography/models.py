from django.apps import apps
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

from .get_from_imdb import ActorInfo

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    daily_api_counter = models.IntegerField(default=0)

class ActorUserManager(models.Manager):

    def register_from_response(self, response, user, phrase):
        for entry in response:
            if 'nm' in entry['id']:
                self.get_or_create(
                    actor = Actor.objects.get(imdb_id=entry['id']),
                    user = user,
                    phrase = phrase
                )          

class ActorUser(models.Model):
    user = models.ForeignKey('filmography.UserProfile', on_delete=models.CASCADE)
    actor = models.ForeignKey('filmography.Actor', on_delete=models.CASCADE)
    phrase = models.CharField(max_length=64) # usunąć

    objects=ActorUserManager()


class ActorManager(models.Manager):

    def register_from_response(self, response):
        for entry in response:
            if 'nm' in entry['id']:
                self.get_or_create(
                    imdb_id=entry['id'],
                    defaults={
                        'fullname': entry['name']
                    }
                )
    
class Actor(models.Model):
    fullname = models.CharField(max_length=128)
    imdb_id = models.CharField(max_length=64, unique=True)

    objects = ActorManager()

class MovieManager(models.Manager):
    def register_from_response(self, response):
        for entry in response:
            self.get_or_create(
                id_from_imdb = entry['id'],
                defaults={
                        'title': entry['title']
                    }
            )


class Movie(models.Model):
    id_from_imdb = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128)

    objects = MovieManager()

class ActorMovieManager(models.Manager):
    def register_from_response(self, response, actor_imdb_id):
        for entry in response:
            self.create(
                actor = Actor.objects.get(imdb_id=actor_imdb_id),
                movie = Movie.objects.get(id_from_imdb=entry['id'])
            )

class ActorMovie(models.Model):
    actor = models.ForeignKey('filmography.Actor', on_delete=models.CASCADE)
    movie = models.ForeignKey('filmography.Movie', on_delete=models.CASCADE)

    objects = ActorMovieManager()

class ActorUserRequest(models.Model):
    user = models.ForeignKey('filmography.UserProfile', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    phrase = models.CharField(max_length=64)
    response = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=1,
        choices=(('p', 'W kolejce'), ('r', 'W trakcie pobierania'), ('e', 'Błąd'), ('d', 'Pobrano')), default='p'
    )

    def set_response(self):
        self.status = 'r'
        self.save()
        x=Actor.objects.filter(fullname__icontains=self.phrase)
        if x:
            self.response="Aktor jest w bazie."
            self.status = 'd'
            self.save()
        else:
            try:
                actor = ActorInfo(settings.API_KEY)
                actors = actor.get_actors_ids(self.phrase)
            except:
                self.status = 'e'
                self.save()
            else:
                self.response = actors
                self.status = 'd'
                self.save()
                apps.get_model('filmography.Actor').objects.register_from_response(self.response)
                x = apps.get_model('filmography.UserProfile').objects.filter(user=self.user.user).first()
                x.daily_api_counter +=1
                x.save()

class MovieRequest(models.Model):
    actor_imdb_id = models.CharField(max_length=64)
    datetime = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=1,
        choices=(('p', 'W kolejce'), ('r', 'W trakcie pobierania'), ('e', 'Błąd'), ('d', 'Pobrano')), default='p'
    )

    def set_response(self):
        self.status = 'r'
        self.save()
        x = Actor.objects.filter(imdb_id=self.actor_imdb_id).first() # Czy jest to konieczne, czy zbędne.
        y = ActorMovie.objects.filter(actor=x.id)
        if y:
            self.response="Filmy znajdują się w bazie."
            self.status = 'd'
            self.save()
        else:
            try:
                actor = ActorInfo(settings.API_KEY)
                movies = actor.get_actor_filmography(self.actor_imdb_id)
            except:
                self.status = 'e'
                self.save()
            else:
                self.response = movies
                self.status = 'd'
                self.save()
                apps.get_model('filmography.Movie').objects.register_from_response(self.response)
                apps.get_model('filmography.ActorMovie').objects.register_from_response(self.response, self.actor_imdb_id)