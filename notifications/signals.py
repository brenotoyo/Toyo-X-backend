from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from posts.models import Like, Comment
from users.models import User
from .models import Notification


@receiver(post_save, sender=Like)
def notify_like(sender, instance, created, **kwargs):
    if not created:
        return
    # Não notifica se curtiu o próprio post
    if instance.user == instance.post.author:
        return
    Notification.objects.create(
        recipient=instance.post.author,
        sender=instance.user,
        type='like',
        post=instance.post,
    )


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if not created:
        return
    # Não notifica se comentou no próprio post
    if instance.user == instance.post.author:
        return
    Notification.objects.create(
        recipient=instance.post.author,
        sender=instance.user,
        type='comment',
        post=instance.post,
    )


@receiver(m2m_changed, sender=User.followers.through)
def notify_follow(sender, instance, action, pk_set, **kwargs):
    if action != 'post_add':
        return
    for pk in pk_set:
        follower = User.objects.get(pk=pk)
        # Não notifica se seguiu a si mesmo
        if follower == instance:
            continue
        Notification.objects.create(
            recipient=instance,
            sender=follower,
            type='follow',
        )