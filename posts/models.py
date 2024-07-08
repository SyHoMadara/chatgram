from django.db import models

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    reply = models.ForeignKey("self", on_delete=models.DO_NOTHING, related_name="replies", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def set_author(self, email):
        self.author = User.objects.get(email=email)

    def set_receiver(self, email):
        self.receiver = User.objects.get(email=email)

    def set_reply(self, post_id):
        self.reply = Post.objects.get(id=post_id)

    @staticmethod
    def create_post(author_email, receiver_email, message):
        post = Post()
        post.set_author(author_email)
        post.set_receiver(receiver_email)
        post.message = message
        post.save()
        return post

    @staticmethod
    def create_reply_message(author_email, receiver_email, message, post_id):
        post = Post.create_post(author_email, receiver_email, message)
        post.set_reply(post_id)
        post.save()
        return post

    def delete(self, using=None, keep_parents=True):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.author} to {self.receiver}: {self.message}"
