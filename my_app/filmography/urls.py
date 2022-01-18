from django.conf.urls import include
from django.urls import path
from filmography.views import ActorMovieListView, register, dashboard, UserProfileView, UpdateUserProfile, ApiRequestHistoryList, ActorRequestHistoryList, ActorListView, usaged_api_chart, actoruserrequestview, Like
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("myprofile/<pk>", UserProfileView.as_view(), name="userprofileview"),
    path("myprofile/<pk>/update", UpdateUserProfile.as_view(), name="updateuserprofile"),
    path("myprofile/<pk>/apirequesthistory/<phrase>", ApiRequestHistoryList.as_view(), name="apirequesthistory"),
    path("myprofile/<pk>/actorrequesthistory", ActorRequestHistoryList.as_view(), name="actorrequesthistory"),
    path("actors", ActorListView.as_view(), name="actorlistview"),
    path("usaged_api_chart/", usaged_api_chart, name="usaged_api_chart"),
    path("actoruserrequestview/<pk>", actoruserrequestview, name="actoruserrequestview"),
    path("myprofile/<pk>/apirequesthistory/<actor>/actormovies", ActorMovieListView.as_view(), name="actormovielistview"),
    path('like/', Like.as_view(), name='like'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)