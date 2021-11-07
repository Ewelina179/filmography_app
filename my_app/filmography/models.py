from django.db import models
from django.contrib.auth.models import AbstractUser

class Movie(models.Model):
    title = models.CharField(max_length=128, unique=True)

class Actor(models.Model):
    fullname = models.CharField(max_length=128)
    movies = models.ManyToManyField(Movie) # musi być coś więcej, żeby odróżnić ludzi o tym samym fullname

class User(AbstractUser):
    pass
    actors = models.ManyToManyField(Actor, through='Favourite') # tu unique? Bo się dodaje w nieskonczoność

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    is_favourite = models.BooleanField() # domyślnie musi być False
