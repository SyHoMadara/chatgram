from rest_framework import serializers

from users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_verified",
            "is_deleted",
            "created_at",
            "updated_at",
            "last_login",
        ]
        read_only_fields = [
            "is_staff",
            "is_active",
            "is_verified",
            "is_deleted",
            "created_at",
            "updated_at",
            "last_login",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        if email := validated_data.get("email"):
            instance.set_email(email)
        return super().update(instance, validated_data)
