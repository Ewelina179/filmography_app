from django.contrib.auth.models import User
from filmography.models import Actor, UserProfile

import pytest

@pytest.fixture
def test_user():
    return User.objects.create_user('ann', 'lennon@thebeatles.com', 'annpassword')

@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1

#@pytest.mark.django_db
#def test_db_user(test_user):
#    userprofile = UserProfile.objects.create(user = test_user)
#    assert UserProfile.user == test_user


@pytest.fixture
def test_actor():
    return Actor.objects.create(fullname = "Natalie Portman", imdb_id = "nm0000204")

@pytest.mark.django_db(True)
def test_actor_in_db(test_actor):
    actor = Actor.objects.get(fullname = "Natalie Portman")
    assert actor == test_actor 

#@pytest.mark.django_db(True)
#def test_actor_in_db_2(test_actor):
#    actor = Actor.objects.get(fullname = "Natalie P")
#    assert actor == test_actor
