from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializer import RegisterUserSerializer, UserSerializer, PublicUserSerializer


class UserRegistrationView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
        operation_description="Register a new user",
        responses={201: RegisterUserSerializer},
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfilesView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={200: UserSerializer},
    )
    @action(detail=False, methods=["get"], url_path="profile", url_name="profile")
    def get_profile(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_description="Update user profile",
        responses={200: UserSerializer},
    )
    @action(detail=False, methods=["post"], url_path="profile", url_name="profile")
    def update_profile(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile successfully updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"errors": e}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body={"password": "string"},
        operation_description="Change user password",
        responses={200: "Password successfully changed"},
    )
    @action(detail=False, methods=["post"], url_path="change-password", url_name="change-password")
    def change_password(self, request):
        user = request.user
        try:
            user.set_password(request.data.get("password"))
            user.save()
            return Response({"message": "Password successfully changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"errors": e}, status=status.HTTP_400_BAD_REQUEST)


# get profile of other users with email
class PublicUserProfileView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={200: UserSerializer},
    )
    @action(detail=False, methods=["get"], url_path="profile", url_name="profile")
    def get_profile(self, request):
        try:
            user = User.objects.get(email=request.data.get("email"))
            serializer = PublicUserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class LogoutUserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout user",
        responses={200: "User successfully logged out"},
    )
    def logout(self, request):
        token = RefreshToken(request.data.get("refresh-token"))
        RefreshToken.for_user(request.user).blacklist()
        token.blacklist()
        return Response({"message": "User successfully logged out"}, status=status.HTTP_200_OK)

