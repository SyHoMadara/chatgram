from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet

router = DefaultRouter()
urlpatterns = [
    path("send/", PostViewSet.as_view({"post": "send"}), name="send_message"),
]
