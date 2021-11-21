from django.conf.urls import url, include
from django.urls import path
from filmography.views import register, dashboard #home, , actors, actor_detail, get_actor

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    #path('actors/<cont>', actors, name="actors"),
    #url(r'^cont/$', actors, name="actors"),
    #url(r"^actor/(?P<nm>\d+)/$", actor_detail, name="actor_detail"),
    #url(r"^search", get_actor, name="get_actor"),
    #path('actor/<str:nm>/<str:fullname>', actor_detail, name="actor_detail"),
]