from django.test import TestCase
from .models import Post
from users.models import User

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
        post = Post.create_reply_message(self.user1.email, self.user2.email, "reply message", self.post.id)
        self.assertEqual(post.reply, self.post)
        self.assertEqual(post.receiver, self.user2)
        self.assertEqual(post.message, "reply message")
        self.assertEqual(post.author, self.user1)

    def test_create_post_without_receiver(self):
        with self.assertRaises(User.DoesNotExist):
            Post.create_post(self.user1.email, "noexist@test.com", "message")

    def test_reply_to_nonexistent_post(self):
        with self.assertRaises(Post.DoesNotExist):
            Post.create_reply_message(self.user1.email, self.user2.email, "reply message", 100)