from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile

# Crear un perfil de usuario cuando se crea un usuario
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Solo se ejecuta cuando el usuario es creado
        UserProfile.objects.create(user=instance)

# Guardar el perfil del usuario cuando el usuario se guarda
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Se asegura que el perfil del usuario se guarda cada vez que se guarda el usuario
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
