from django.conf.urls import url, include
from django.urls import path
from filmography.views import register, dashboard, UserProfile, UpdateUserProfile
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("myprofile/<pk>", UserProfile.as_view()),
    path("myprofile/<pk>/update", UpdateUserProfile.as_view()),
    #path("search", ActorUserRequestFormView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)