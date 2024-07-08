from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    LogoutUserView,
    PublicUserProfileView,
    UserProfilesView,
    UserRegistrationView,
)

router = DefaultRouter()

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "profile/", UserProfilesView.as_view({"get": "get_profile"}), name="get_profile"
    ),
    path(
        "change-profile/",
        UserProfilesView.as_view({"post": "update_profile"}),
        name="change_profile",
    ),
    path(
        "change-password/",
        UserProfilesView.as_view({"post": "change_password"}),
        name="change_password",
    ),
    path("logout/", LogoutUserView.as_view({"post": "logout"}), name="logout"),
    path(
        "user/",
        PublicUserProfileView.as_view({"post": "get_profile"}),
        name="get_public_profile",
    ),
]
