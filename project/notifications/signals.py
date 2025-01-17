from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from mi_blog.models import Post
from friends.models import FriendlySent
from django.db import models

@receiver(post_save, sender=Post)
def create_notification_for_friend(sender, instance, created, **kwargs):
    if created:
        # Filtrar las amistades aceptadas
        friendships = FriendlySent.objects.filter(
            (models.Q(from_user=instance.author) | models.Q(to_user=instance.author)),
            status=FriendlySent.Status.ACEPPTED
        )

        # Crear una notificación para cada amigo
        for friendship in friendships:
            friend = friendship.to_user if friendship.from_user == instance.author else friendship.from_user
            message = f"{instance.author.username} ha hecho una nueva publicación"
            Notification.objects.create(user=friend, message=message, post=instance)