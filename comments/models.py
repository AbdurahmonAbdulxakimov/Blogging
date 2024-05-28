from django.db import models
from django.contrib.auth import get_user_model

from posts.models import Post, TimeStampedModel


User = get_user_model()


class Comment(TimeStampedModel):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return self.user.username + " | " + self.post.title

