from datetime import timezone

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from posts.models import Post, Status, PostViews


@receiver(pre_save, sender=Post)
def set_published_date(sender, instance, **kwargs):
    if instance.status == Status.ACCEPTED and not instance.published_date:
        instance.published_date = timezone.now()
    return instance


@receiver(post_save, sender=PostViews)
def update_post_views_count(sender, instance, **kwargs):
    instance.post.views_count = instance.post.views_count + 1
    instance.post.save()
    return instance
