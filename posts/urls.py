from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet

router = DefaultRouter()
urlpatterns = [
    path("send/", PostViewSet.as_view({"post": "send"}), name="send_message"),
    path(
        "posts-list-<int:pk>/",
        PostViewSet.as_view({"get": "retrieve"}),
        name="posts_list",
    ),
    path(
        "edit-post-<int:pk>/", PostViewSet.as_view({"post": "edit"}), name="post_edit"
    ),
    path(
        "delete-post-<int:pk>/",
        PostViewSet.as_view({"delete": "delete"}),
        name="post_delete",
    ),
]
