from django.db import models
from django.conf import settings

# Create your models here.

class Solicitud_Send(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=FriendlySent.Status.SENT)

class FriendlySent(models.Model):


    class Status(models.TextChoices):
        SENT = 'SE', 'SENT'
        ACEPPTED = 'AC', 'ACEPPTED'
        RECHAZED = 'RE', 'RECHAZED'
        PENDING = 'PE', 'PENDING'

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, 
                                related_name='friend_requests_sent')

    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, 
                                related_name='friend_requests_received') 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=6, 
                            choices=Status.choices, 
                            default=Status.SENT )

            
    objects = models.Manager()
    enviado = Solicitud_Send()
    

    def aceptar(self):
        self.status = self.Status.ACEPPTED
        self.save()

    # Método para rechazar la solicitud
    def rechazar(self):
        self.status = self.Status.RECHAZED
        self.save()
    
    def eliminar_amistad(self):
        if self.status == self.Status.ACEPPTED:
            self.delete()

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"
    class Meta:
        unique_together = ('from_user', 'to_user')


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='follower')
    
    following = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='following')
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Asegura que un usuario no pueda seguir a otro más de una vez

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"