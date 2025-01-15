from django.db import models
from django.conf import settings

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Preferencias generales
    dark_mode = models.BooleanField(default=False)  # Modo oscuro
    language = models.CharField(max_length=10, default='en')  # Idioma
    timezone = models.CharField(max_length=100, default='UTC')  # Zona horaria
    date_format = models.CharField(max_length=50, default='YYYY-MM-DD')  # Formato de fecha
    notifications_enabled = models.BooleanField(default=True)  # Activar notificaciones

    # Preferencias de cuenta
    email_verified = models.BooleanField(default=False)  # Verificación del correo electrónico
    two_factor_auth = models.BooleanField(default=False)  # Autenticación de dos factores
    account_visibility = models.CharField(max_length=50, choices=[('public', 'Public'), ('private', 'Private')], default='public')  # Visibilidad de la cuenta

    # Preferencias de interfaz
    theme = models.CharField(max_length=50, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')  # Tema visual
    font_size = models.CharField(max_length=50, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], default='medium')  # Tamaño de fuente
    sidebar_position = models.CharField(max_length=50, choices=[('left', 'Left'), ('right', 'Right')], default='left')  # Posición de la barra lateral

    # Preferencias de privacidad
    share_activity = models.BooleanField(default=False)  # Compartir actividad con amigos
    data_sharing = models.BooleanField(default=False)  # Compartir datos con terceros
    hide_profile_picture = models.BooleanField(default=False)  # Ocultar foto de perfil

    # Configuraciones de seguridad
    password_expiry_days = models.IntegerField(default=90)  # Vencimiento de la contraseña
    login_attempts_limit = models.IntegerField(default=5)  # Intentos de inicio de sesión fallidos
    allow_social_logins = models.BooleanField(default=True)  # Permitir inicio de sesión con redes sociales

    # Preferencias de notificaciones
    email_notifications = models.BooleanField(default=True)  # Notificaciones por correo electrónico
    sms_notifications = models.BooleanField(default=False)  # Notificaciones por SMS
    push_notifications = models.BooleanField(default=False)  # Notificaciones push

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

