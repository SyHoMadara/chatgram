from django.test import TestCase
from django.urls import reverse

from users.models import User

from .models import Post

PASSWORD = "k5c2xSW5"


class PostTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user1 = User.objects.create_user(email="user1@test.com", password=PASSWORD)
        cls.user2 = User.objects.create_user(email="user2@test.com", password=PASSWORD)
        cls.post = Post(author=cls.user1, receiver=cls.user2, message="Hello, World!")
        cls.post.save()

    def test_creating_post(self):
        post = Post.create_post(self.user1.email, self.user2.email, "new message")
        self.assertEqual(post.receiver, self.user2)
        self.assertEqual(post.message, "new message")
        self.assertEqual(post.author, self.user1)

    def test_reply_post(self):
        post = Post.create_reply_message(
            self.user1.email, self.user2.email, "reply message", self.post.id
        )
        self.assertEqual(post.reply, self.post)
        self.assertEqual(post.receiver, self.user2)
        self.assertEqual(post.message, "reply message")
        self.assertEqual(post.author, self.user1)

    def test_create_post_without_receiver(self):
        with self.assertRaises(User.DoesNotExist):
            Post.create_post(self.user1.email, "noexist@test.com", "message")

    def test_reply_to_nonexistent_post(self):
        with self.assertRaises(Post.DoesNotExist):
            Post.create_reply_message(
                self.user1.email, self.user2.email, "reply message", 100
            )


def login(self, email, password):
    url = reverse("token_obtain_pair")
    data = {"email": email, "password": password}
    response = self.client.post(url, data)
    return response.data["access"], response.data["refresh"]


class PostApiTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user1 = User.objects.create_user(email="user1@test.com", password=PASSWORD)
        cls.user2 = User.objects.create_user(email="user2@test.com", password=PASSWORD)
        cls.post = Post.create_post(cls.user1.email, cls.user2.email, "Hello, World!")

    def test_send_message(self):
        url = reverse("send_message")
        access, _ = login(self, self.user1.email, PASSWORD)
        data = {"receiver": self.user2.email, "message": "New Message"}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access}")
        self.assertEqual(response.status_code, 201)

    def test_reply_message(self):
        url = reverse("send_message")
        access, _ = login(self, self.user1.email, PASSWORD)
        data = {"message": "Reply message", "reply": str(self.post.id)}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f"Bearer {access}")

        self.assertEqual(response.status_code, 201)

    def test_post_list(self):
        url = reverse("posts_list", kwargs={"pk": self.user2.id})
        access_token, _ = login(self, self.user1.email, PASSWORD)
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        url = reverse("post_edit", kwargs={"pk": self.post.id})
        access_token, _ = login(self, self.user1.email, PASSWORD)
        data = {"message": "Edited message"}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.get(id=self.post.id).message, data["message"])

    def test_delete_post(self):
        url = reverse("post_delete", kwargs={"pk": self.post.id})
        access_token, _ = login(self, self.user1.email, PASSWORD)
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEqual(response.status_code, 204)
        self.assertTrue(Post.objects.get(id=self.post.id).is_deleted)
