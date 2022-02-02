from django.contrib.auth.models import User
from filmography.models import Actor, UserProfile, Movie, ActorMovie
from filmography.models import ActorUser

import pytest

#@pytest.mark.django_db
#def test_new_user(user_factory):
#    user = user_factory.create()
#    count = User.objects.all().count()
    #print(user.username)
    #print(count)
#    assert True

@pytest.fixture
def user():
    return User.objects.create_user('ann', 'lennon@thebeatles.com', 'annpassword')

#@pytest.fixture
#def userprofile(user):
#    return UserProfile.objects.create(user=user, first_name="Jan", last_name="Kowalski")

#@pytest.mark.django_db
#def test_user_create():
#   User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#    assert User.objects.count() == 1

@pytest.fixture
def actor():
    return Actor.objects.create(fullname = "Natalie Portman", imdb_id = "nm0000204")

@pytest.mark.django_db
def test_actor_in_db(actor):
    actor = Actor.objects.get(fullname = "Natalie Portman")
    assert actor == actor 

#@pytest.mark.django_db(True)
#def test_actor_in_db_2(test_actor):
#    actor = Actor.objects.get(fullname = "Natalie P")
#    assert actor == test_actor

@pytest.fixture
def actoruser(actor, user):
    return ActorUser.objects.create(userprofile=user.userprofile, actor=actor)

@pytest.mark.django_db
def test_actor_user_in_db(actor, user):
    return ActorUser.objects.filter(actor=actor, user=user.userprofile).exists()

@pytest.mark.django_db
def test_userprofile(user):
    user.userprofile.first_name = "Anna"
    user.save()
    assert user.userprofile.first_name == "Anna"

@pytest.fixture
def movie():
    return Movie.objects.create(id_from_imdb="nm12345", title="ABC")

@pytest.fixture
def actormovie(actor, movie):
    return ActorMovie.objects.create(actor=actor, movie=movie)

@pytest.mark.django_db
def test_actor_movie_in_db(actor, movie):
    return ActorMovie.objects.filter(actor=actor, movie=movie).exists()