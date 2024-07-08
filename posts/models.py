from django.db import models

from users.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    reply = models.ForeignKey("self", on_delete=models.DO_NOTHING, related_name="replies", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} to {self.receiver}: {self.message}"
