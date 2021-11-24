from django.conf.urls import url, include
from django.urls import path
from filmography.views import register, dashboard, UserProfileView, UpdateUserProfile, usaged_api_chart, actoruserrequestview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("myprofile/<pk>", UserProfileView.as_view(), name="userprofileview"),
    path("myprofile/<pk>/update", UpdateUserProfile.as_view(), name="updateuserprofile"),
    path("usaged_api_chart/", usaged_api_chart, name="usaged_api_chart"),
    path("actoruserrequestview", actoruserrequestview, name="actoruserrequestview"),
    #path("search", ActorUserRequestFormView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)