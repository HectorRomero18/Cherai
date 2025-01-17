from .models import Notification

def add_post_urls(request):
    # Asegúrate de manejar usuarios no autenticados
    if not request.user.is_authenticated:
        return {}

    notifications = Notification.objects.filter(user=request.user)

    for notification in notifications:
        if notification.post:
            notification.post_absolute_url = notification.post.get_absolute_url()
    return {'notifications': notifications}

def image_user(request):
    # Asegúrate de manejar usuarios no autenticados
    if not request.user.is_authenticated:
        return {}

    notifications = Notification.objects.filter(user=request.user)
    context = {'image_profile': None}
    
    for notification in notifications:
        if notification.post:  # Verificar si la notificación tiene un post asociado
            author = notification.post.author  # Obtener el autor de la publicación
            
            # Verificar si el autor tiene una imagen de perfil
            if author and hasattr(author, 'image_profile'):
                context['image_profile'] = author.image_profile
                break

    return context
