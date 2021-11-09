from django.conf.urls import url
from filmography.views import home, dashboard, actors, actor_detail, get_actor

urlpatterns = [
    url(r"^home/", home, name="home"),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^actors", actors, name="actors"),
    url(r"^actor/(?P<nm>\D+)", actor_detail, name="actor_detail"),
    url(r"^search", get_actor, name="get_actor"),
]