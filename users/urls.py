from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    LogoutUserView,
    PublicUserProfileView,
    UserProfilesView,
    UserRegistrationView,
    sign_up,
    login,
)

router = DefaultRouter()

urlpatterns = [
    path("api/register/", UserRegistrationView.as_view(), name="register"),
    path(
        "api/profile/", UserProfilesView.as_view({"get": "get_profile"}), name="get_profile"
    ),
    path(
        "api/change-profile/",
        UserProfilesView.as_view({"post": "update_profile"}),
        name="change_profile",
    ),
    path(
        "api/change-password/",
        UserProfilesView.as_view({"post": "change_password"}),
        name="change_password",
    ),
    path("api/logout/", LogoutUserView.as_view({"post": "logout"}), name="logout"),
    path(
        "api/user/",
        PublicUserProfileView.as_view({"post": "get_profile"}),
        name="get_public_profile",
    ),
    path("signup/", sign_up, name="sign_up"),
    path("login/", login, name="login")

]
