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
    phrase = models.CharField(max_length=64)

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

class ActorUserRequestManager(models.Manager):
    def check_is_in_db(self, response):
        lst_of_actors = []
        for entry in response:
            if self.get(actor = Actor.objects.get(imdb_id=entry['id'])):
                lst_of_actors.append(entry)
        return lst_of_actors
# szukaj po frazie id aktora w bazie aktor id imdb jak są pasujący to zrób ich listę ze słowników jak w response żeby wypluło to samo co do register from response actoruser, zeby tam zapisało tego aktora

class ActorUserRequest(models.Model):
    user = models.ForeignKey('filmography.UserProfile', on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    phrase = models.CharField(max_length=64)
    response = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=1,
        choices=(('p', 'W kolejce'), ('r', 'W trakcie pobierania'), ('e', 'Błąd'), ('d', 'Pobrano')), default='p'
    )

    objects = ActorUserRequestManager()

    def set_response(self):
        self.status = 'r'
        self.save()
        try: # nie wiem jak to wyciągnąć po frazie. z manadżerem? atrybut fraza w modelu aktor to raczej nie jest dobry pomysł
            try:
                self.objects.check_is_in_db(self.phrase)
                apps.get_model('filmography.ActorUser').objects.register_from_response(self.objects.check_is_in_db(self.phrase), self.user, self.phrase)
                print("Coś")
                self.status = 'd'
            except:
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
            apps.get_model('filmography.ActorUser').objects.register_from_response(self.response, self.user, self.phrase)
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
        try:
            # duo uzupełnienia kiedy ActorUserRequets będzie poprawnie. sprawdż czy jest w bazie. jeśli tak, status d. jeśli nie dopiero to co niżej
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