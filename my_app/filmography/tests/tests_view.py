from django.urls import reverse
from filmography.views import ActorListView

import pytest 

@pytest.mark.django_db
def test_view(client):
   url = reverse('register')
   response = client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_actor_list_view_response(client):
   url = reverse("actorlistview")
   response = client.get(url)
   content = response.content.decode(response.charset)
   assert response.status_code == 200 # bez login required 200
   assert "Lista aktorów" in content
