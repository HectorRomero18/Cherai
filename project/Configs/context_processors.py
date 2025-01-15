# context_processors.py
from .models import UserProfile

def user_config(request):
    if request.user.is_authenticated:
        perfil = request.user.userprofile
        return {
            'dark_mode': perfil.dark_mode,
            'language': perfil.language,  # Si tienes un campo de idioma
            'notifications_enabled': perfil.notifications_enabled,  # Si tienes configuraciones de notificaciones
            # Puedes agregar más configuraciones aquí según lo necesites
        }
    return {
        'dark_mode': False,  # Valor por defecto
        'language': 'es',     # Idioma por defecto
        'notifications_enabled': True,  # Valor por defecto para notificaciones
    }
