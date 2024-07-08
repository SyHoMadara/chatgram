from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post
from .serializer import PostCreatingSerializer


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreatingSerializer

    @staticmethod
    def identify_receiver(post: Post, user):
        if post.receiver == user:
            return post.author
        return post.receiver

    @swagger_auto_schema(method="post", request_body=PostCreatingSerializer)
    @action(
        detail=False, methods=["post"], url_name="send_message", url_path="send-message"
    )
    def send(self, request):
        serializer = self.get_serializer(data=request.data)
        reply = request.data.get("reply")
        if serializer.is_valid():
            try:
                # check if the user is replying to his own post
                if reply:
                    post = self.queryset.get(id=reply)
                    if post.author != request.user and post.receiver != request.user:
                        return Response(
                            {"error": "You can't reply to this post"},
                            status=status.HTTP_403_FORBIDDEN,
                        )
                    serializer.save(
                        author=request.user,
                        receiver=self.identify_receiver(post, request.user),
                    )
                else:
                    serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # # get all posts
    # def list(self, request, *args, **kwargs):
    #     queryset = self.queryset.filter(receiver=request.user)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # # get a post by id
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    #
    # # update a post by id
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    #
    # # delete a post by id
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # # send a message to user by id
    # @swagger_auto_schema(method="post", request_body=PostCreatingSerializer)
    # @action(detail=True, methods=["post"])
    # def send_message(self, request, pk=None):
    #     receiver = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(author=request.user, receiver=receiver)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # # edit a message by id
    # @swagger_auto_schema(method="put", request_body=PostCreatingSerializer)
    # @action(detail=True, methods=["put"])
    # def edit_message(self, request, pk=None):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    #
    # # delete a message by id
    # @action(detail=True, methods=["delete"])
    # def delete_message(self, request, pk=None):
    #     instance = self
