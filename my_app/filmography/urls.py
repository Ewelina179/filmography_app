from django.conf.urls import url
from filmography.views import home, dashboard

urlpatterns = [
    url(r"^home/", home, name="home"),
    url(r"^dashboard/", dashboard, name="dashboard"),
]