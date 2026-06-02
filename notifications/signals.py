from django.db.models.signals import post_save
from django.dispatch import receiver
from comments.models import PostLike, CommentLike, Comment
from profiles.models import Follow
from .models import Notification


@receiver(post_save, sender=PostLike)
def notify_post_like(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type='like',
            message=f'{instance.user.username} liked your post.'
        )


@receiver(post_save, sender=CommentLike)
def notify_comment_like(sender, instance, created, **kwargs):
    if created and instance.user != instance.comment.author:
        Notification.objects.create(
            recipient=instance.comment.author,
            sender=instance.user,
            notification_type='like',
            message=f'{instance.user.username} liked your comment.'
        )


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.author,
            notification_type='comment',
            message=f'{instance.author.username} commented on your post.'
        )


@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type='follow',
            message=f'{instance.follower.username} started following you.'
        )