from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from members.views import MemberProfile, MemberViewSet
from posts.views import BoardViewSet, PostAPIView

router = routers.DefaultRouter()
router.register(r"members", MemberViewSet)
router.register(r"posts", BoardViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/apiview/members/", MemberProfile.as_view(), name="member-profile"),
    path("api/apiview/posts/", PostAPIView.as_view(), name="post-list"),
]
