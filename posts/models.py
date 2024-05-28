from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Status(models.TextChoices):
    REJECTED = 'rejected'
    IN_MODERATION = 'in_moderation'
    ACCEPTED = 'accepted'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Tag(TimeStampedModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class Post(TimeStampedModel):
    cover_image = models.ImageField()
    title = models.CharField(max_length=200)
    content = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey('posts.Category', on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('posts.Tag', related_name='posts', blank=True)

    status = models.CharField(choices=Status.choices, default=Status.IN_MODERATION, max_length=16)
    views_count = models.PositiveIntegerField(default=0)

    published_date = models.DateTimeField('date published', blank=True, null=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title


class PostViews(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    ip = models.GenericIPAddressField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")

    class Meta:
        verbose_name = 'post views'
        verbose_name_plural = 'post views'
        unique_together = (('ip', 'user'),)
