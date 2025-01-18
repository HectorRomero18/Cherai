from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendlySent, Follow
from mi_blog.models import User  # Importa el modelo User personalizado
from django.db.models import Q
from django.utils.text import slugify

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)

    # Verificar si el usuario intenta enviarse una solicitud a sí mismo
    if to_user == request.user:
        messages.error(request, "No puedes enviarte una solicitud a ti mismo.")
        return redirect('mi_blog:lista_usuarios')  # Redirige a la lista de usuarios

    # Verificar si ya son amigos (si ya hay una relación de amistad registrada)
    if FriendlySent.objects.filter(from_user=request.user, to_user=to_user, status=FriendlySent.Status.ACEPPTED).exists() or \
       FriendlySent.objects.filter(from_user=to_user, to_user=request.user, status=FriendlySent.Status.ACEPPTED).exists():
        messages.info(request, "Ya son amigos.")
        return redirect('mi_blog:lista_usuarios')

    # Verificar si ya existe una solicitud de amistad enviada
    if FriendlySent.objects.filter(from_user=request.user, to_user=to_user, status=FriendlySent.Status.SENT).exists() or \
        FriendlySent.objects.filter(from_user=to_user, to_user=request.user, status=FriendlySent.Status.SENT).exists():
        messages.info(request, "Ya has enviado una solicitud de amistad a este usuario.")
        return redirect('mi_blog:lista_usuarios')

    # Verificar si hay una solicitud de amistad pendiente para aceptar o rechazar
    if FriendlySent.objects.filter(from_user=to_user, to_user=request.user, status=FriendlySent.Status.PENDING).exists():
        messages.info(request, "Tienes una solicitud pendiente de este usuario.")
        return redirect('mi_blog:lista_usuarios')

    # Si no hay solicitudes previas, se envía una nueva solicitud
    FriendlySent.objects.create(from_user=request.user, to_user=to_user, status=FriendlySent.Status.SENT)
    messages.success(request, f"Has enviado una solicitud de amistad a {to_user.username}.")
    return redirect('mi_blog:lista_usuarios')


@login_required
def accept_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)

    # Obtén la solicitud de amistad pendiente
    friendship = get_object_or_404(FriendlySent, from_user=to_user, to_user=request.user, status=FriendlySent.Status.SENT)

    # Acepta la solicitud
    friendship.aceptar()
    messages.success(request, f"Ahora eres amigo de {to_user.username}.")
    return redirect('mi_blog:home')  

@login_required
def reject_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)

    # Obtén la solicitud de amistad pendiente
    friendship = get_object_or_404(FriendlySent, from_user=to_user, to_user=request.user, status=FriendlySent.Status.SENT)

    # Rechaza la solicitud
    friendship.rechazar()
    messages.success(request, f"Has rechazado la solicitud de amistad de {to_user.username}.")
    return redirect('mi_blog:home')  


@login_required
def friend_requests(request):
    received_requests = FriendlySent.objects.filter(
        to_user = request.user,
        status = FriendlySent.Status.SENT
    )
    return render(request, 'friends/friend_requests.html', {'received_requests': received_requests}) 

@login_required
def delete_friend(request, username):

    user = get_object_or_404(User, username=username)

    try:
        # Intenta obtener una relación de amistad única
        friendship = FriendlySent.objects.get(
            Q(from_user=request.user, to_user=user, status=FriendlySent.Status.ACEPPTED) |
            Q(from_user=user, to_user=request.user, status=FriendlySent.Status.ACEPPTED)
        )

        friendship.eliminar_amistad()  # Elimina la amistad
        messages.success(request, f"Has eliminado a {user.username} de tu lista de amigos.")

    except FriendlySent.DoesNotExist:
        messages.error(request, "No se encontró ninguna relación de amistad con este usuario.")
    
    return redirect('mi_blog:perfilOne', username=request.user, slug=slugify(request.user))

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, username=user_id)
    
    if user_to_follow != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
        if not created:
            messages.info(request, "Ya sigues a este usuario.")
        else:
            messages.success(request, f"Ahora sigues a {user_to_follow.username}.")
    return redirect('mi_blog:lista_usuarios')

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, username=user_id)
    
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    messages.success(request, f"Has dejado de seguir a {user_to_unfollow.username}.")
    return redirect('friends:show_my_followings')

@login_required
def show_followers(request):
    followed_users = User.objects.filter(follower__following=request.user)
    return render(request, 'friends/follow.html', {'followed_users': followed_users})

@login_required
def show_my_followings(request):
    following_users = User.objects.filter(following__follower=request.user)
    return render(request, 'friends/followings.html', {'followings_users': following_users})
