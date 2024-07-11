from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post
from .serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @staticmethod
    def identify_receiver(post: Post, user):
        if post.receiver == user:
            return post.author
        return post.receiver

    @swagger_auto_schema(method="post", request_body=PostSerializer)
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

    # get all posts
    @swagger_auto_schema(
        method="get",
        responses={200: PostSerializer(many=True)},
        request_body=PostSerializer,
    )
    @action(detail=False, methods=["get"], url_name="posts_list", url_path="posts-list")
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            queryset = self.queryset.filter(
                author=request.user, receiver=pk, is_deleted=False
            )
            for post in queryset:
                post.seen = True
                post.save()
            return Response(
                self.get_serializer(queryset, many=True).data, status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Edit post by id
    @swagger_auto_schema(method="post", request_body=PostSerializer)
    @action(detail=False, methods=["post"], url_name="post_edit", url_path="edit-post")
    def edit(self, request, *args, **kwargs):
        message = request.data.get("message")
        if message:
            try:
                post = self.queryset.get(id=kwargs.get("pk"))
                if post.author == request.user:
                    post.message = request.data.get("message")
                    post.save()
                    post = self.queryset.get(id=kwargs.get("pk"))
                    return Response(
                        PostSerializer(post).data, status=status.HTTP_200_OK
                    )
                return Response(
                    {"error": "You can't edit this post"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            except Post.DoesNotExist:
                return Response(
                    {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

    # delete a post by id
    @swagger_auto_schema(method="delete", responses={204: "No Content"})
    @action(
        detail=False, methods=["delete"], url_name="post_delete", url_path="delete-post"
    )
    def delete(self, request, *args, **kwargs):
        try:
            post = self.queryset.get(id=kwargs.get("pk"))
            if post.author == request.user:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"error": "You can't delete this post"},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
