from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User

from .models import Post


# Serializer for sending message to user with email
class PostCreatingSerializer(ModelSerializer):
    receiver = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.all(), required=False
    )
    reply = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Post
        fields = ["id", "receiver", "message", "reply"]
        read_only_fields = ["id"]
