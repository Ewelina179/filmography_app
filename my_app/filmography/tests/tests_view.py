from django.urls import reverse
from filmography.views import ActorListView
import uuid

import pytest


@pytest.fixture
def test_password():
   return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user


@pytest.mark.django_db
def test_register_view(client):
   url = reverse('register')
   response = client.get(url)
   assert response.status_code == 200


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login


@pytest.mark.django_db
def test_actor_list_view_response(auto_login_user):
   url = reverse("actorlistview")
   client, user = auto_login_user()
   response = client.get(url)
   content = response.content.decode(response.charset)
   assert response.status_code == 200
   assert "Lista aktorów" in content
   #assert response.content_type == "text\html"

@pytest.mark.django_db
def test_post_dashboard(auto_login_user):
   url = reverse("dashboard")
   client, user = auto_login_user()
   response = client.post(url, {"phrase": "Felicity Jones"})
   assert response.status_code == 302

def test_post_dashboard(client, django_user_model):
    username = "user1"
    password = "bar"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    response = client.get("/")
    assert response.status_code == 200