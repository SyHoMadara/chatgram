from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserProfilesView, UserRegistrationView, PublicUserProfileView, LogoutUserView

router = DefaultRouter()

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("profile/", UserProfilesView.as_view({"get": "get_profile"}), name="get-profile"),
    path("change-profile/", UserProfilesView.as_view({"post": "update_profile"}), name="change-profile"),
    path("logout/", LogoutUserView.as_view({"post": "logout"}), name="logout"),
    path("user/", PublicUserProfileView.as_view({"post": "get_profile"}), name="public-profile"),
]
