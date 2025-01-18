from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, User, PostLike
from taggit.models import Tag
from friends.models import FriendlySent, Follow
from datetime import datetime
from django.utils.text import slugify
from .forms import UserProfileForm, CustomLoginForm, CommentsForm, SearchForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required 
from django.views.decorators.http import require_POST 
from django.http import HttpResponse
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q, Count
from django.contrib.auth import get_user_model

 

# Create your views here.
# Mostrar_Post
@login_required
def Mostrar_Post(request):
    posts = Post.published.all().annotate(likes_count=Count('postLike'))

    return render(request, 'blog/post/home.html', {'posts': posts})


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if PostLike.objects.filter(post=post, user=user).exists():
        PostLike.remove_like(post, user)
    else:
        PostLike.objects.create(post=post, user=user)
    return redirect('mi_blog:home')


@login_required
def mostrar_usuarios(request):
    users = User.objects.all()
    
    # Crear un diccionario para pasar las variables adicionales
    user_data = {}
    for user in users:
        # Verifica si el usuario actual y el usuario iterado son amigos
        are_friends = FriendlySent.objects.filter(
            from_user=request.user, to_user=user, status=FriendlySent.Status.ACEPPTED
        ).exists() or FriendlySent.objects.filter(
            from_user=user, to_user=request.user, status=FriendlySent.Status.ACEPPTED
        ).exists()

        # Verifica si hay solicitud de amistad recibida
        friend_request_received = FriendlySent.objects.filter(
            from_user=user, to_user=request.user, status=FriendlySent.Status.PENDING
        ).exists()

        # Verifica si hay solicitud de amistad enviada
        friend_request_sent = FriendlySent.objects.filter(
            from_user=request.user, to_user=user, status=FriendlySent.Status.PENDING
        ).exists()

        # Añadir los valores al diccionario
        user_data[user] = {
            'are_friends': are_friends,
            'friend_request_received': friend_request_received,
            'friend_request_sent': friend_request_sent
        }
    
    return render(request, 'blog/post/users.html', {'users': users, 'user_data': user_data})

# article_create
@login_required
def article_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        publish_date = request.POST.get('publish_date')
        image = request.FILES.get('image')
        tags_input = request.POST.get('tags')

        # Validar y convertir el campo publish_date
        if publish_date:
            publish_date = parse_datetime(publish_date)
            if not publish_date:
                publish_date = datetime.now()  # Fecha y hora actual si el formato no es válido
        else:
            publish_date = datetime.now()  # Asignar fecha y hora actual si no se proporcionó

        # Crear el post
        post = Post.objects.create(
            title=title,
            body=content,
            author=request.user,
            publish=publish_date,
            status=Post.Status.PUBLISHED,  # Asignar el estado como PUBLISHED
            image=image
        )

        # Generar el slug basado en el título
        post.slug = slugify(post.title)
        post.save()  # Guardar el post con el slug generado

        if tags_input:
            tag_names = [tag.strip() for tag in tags_input.split(',')]
            for tag_name in tag_names:
                post.tags.add(tag_name)

        return redirect('mi_blog:home')

    return render(request, 'blog/post/crear.html')

@login_required
def post_detail(request, year, month, day, slug_post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, 
                            slug=slug_post, 
                            publish__year=year, 
                            publish__month=month, 
                            publish__day=day)
    
    # Filtrar los comentarios activos
    comments = post.comments.filter(active=True)
    post_url = request.build_absolute_uri(post.get_absolute_url())

    # Crear el formulario para los comentarios
    form = CommentsForm()
    return render(request, 'blog/post/detalles.html', {'post': post, 'form': form, 'comments': comments, 'post_url': post_url} )

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('mi_blog:home')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'blog/post/perfil.html', {'form': form, 'user': user})

@login_required
def delete_profile_image(request):
    user = request.user

    try:
        # Intenta eliminar la imagen si existe
        if user.image_profile:
            user.image_profile.delete(save=True)  # Borra el archivo físico
            user.image_profile = None  # Limpia el campo en la base de datos
            user.save()
    except ValueError:
        # Si se produce un ValueError, no hay imagen asociada y se ignora
        pass

    return redirect('mi_blog:profile')

def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('mi_blog:home')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = CustomLoginForm()
    return render(request, 'account/login.html', {'form': form})

def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('mi_blog:login') 


def custom_register(request):
    User = get_user_model()
    username = ''
    email = ''
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Validar contraseñas coincidentes
        if password != confirm_password:
            messages.error(request, '¡Las contraseñas no coinciden!')
            return redirect('mi_blog:register')

        # Validar campos vacíos
        if not username or not email or not password:
            messages.error(request, '¡Debes completar todos los campos!')
            return redirect('mi_blog:register')

        # Validar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario no está disponible.')
            return redirect('mi_blog:register')

        # Validar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('mi_blog:register')

        
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, '¡Tu cuenta ha sido creada exitosamente!')
        return redirect('mi_blog:login')

    return render(request, 'account/login.html', {
        'username': username,
        'email': email,
    })


@login_required
@require_POST
def post_comment(request, post_id):
    
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentsForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.name = request.user
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'form': form,
                                                     'post': post, 
                                                     'comment': comment})



def Search(request):
    form = SearchForm(request.GET)  # Utiliza request.GET para pre-poblar el formulario
    query = None
    results = []


    if form.is_valid():  # Si el formulario es válido
        query = form.cleaned_data['query']
        # Realiza la búsqueda utilizando SearchVector
        search_query = SearchQuery(query, search_type='plain')
        results = Post.published.annotate(
            search=SearchVector('title', 'body'),
            rank=SearchRank(SearchVector('title', 'body'), search_query)
        ).filter(search=search_query).order_by('-rank')

    return render(request, 'blog/post/home.html', {
        'form': form,
        'query': query,
        'results': results
    })

def mostrar_perfil(request, username, slug):
    # Obtener el usuario basado en el username
    user = get_object_or_404(User, username=username)

    followers = user.follower.all()  # Los seguidores del usuario
    following = user.following.all()  # Las personas que sigue el usuario

    # Obtener las publicaciones del usuario
    posts = Post.published.filter(author=user)

    # Obtener los amigos del usuario (solicitudes aceptadas)
    amigos = User.objects.filter(
        Q(friend_requests_sent__to_user=user, friend_requests_sent__status=FriendlySent.Status.ACEPPTED) |
        Q(friend_requests_received__from_user=user, friend_requests_received__status=FriendlySent.Status.ACEPPTED)
    ).distinct()

    # Verificar el estado de amistad
    are_friends = FriendlySent.objects.filter(
        Q(from_user=request.user, to_user=user, status=FriendlySent.Status.ACEPPTED) |
        Q(from_user=user, to_user=request.user, status=FriendlySent.Status.ACEPPTED)
    ).exists()

    # Verificar si hay una solicitud pendiente enviada
    friend_request_sent = FriendlySent.objects.filter(
        from_user=request.user, to_user=user, status=FriendlySent.Status.SENT
    ).exists()

    # Verificar si hay una solicitud pendiente recibida
    friend_request_received = FriendlySent.objects.filter(
        from_user=user, to_user=request.user, status=FriendlySent.Status.SENT
    ).exists()

    # Verificar que el slug sea válido (opcional si no es necesario en el modelo)
    if slug != slugify(user.first_name) and slug != slugify(user.username):
        # Si el slug no coincide, redirige al perfil correcto
        return redirect('mi_blog:perfilOne', username=username, slug=slugify(user.username))
    
    # Pasar el conteo de seguidores y seguidos a la plantilla
    return render(request, 'blog/post/perfilOne.html', {
        'user': user,
        'posts': posts,
        'amigos': amigos,
        'are_friends': are_friends,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'followers_count': followers.count(),  # Conteo de seguidores
        'following_count': following.count(),  # Conteo de seguidos
        'follower': followers,
        'following': following
    })

@login_required
def show_my_friends(request, username):
    user = get_object_or_404(User, username=username)

    # Filtramos las relaciones de amistad aceptadas entre el usuario y sus amigos
    amigos = User.objects.filter(
        Q(friend_requests_sent__to_user=user, friend_requests_sent__status=FriendlySent.Status.ACEPPTED) |
        Q(friend_requests_received__from_user=user, friend_requests_received__status=FriendlySent.Status.ACEPPTED)
    ).distinct()

    return render(request, 'blog/post/amigos.html', {'amigos': amigos})


@login_required
def EliminarPost(request, post_id):

    
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        if post.author != request.user:
            messages.error(request, 'No tienes permiso para borrar este post!')
            return redirect('mi_blog:perfilOne', username=post.author.username, slug=post.slug)
        post.delete()
            
        return redirect('mi_blog:perfilOne', username=post.author.username, slug=post.slug)
    return render(request,'blog/post/delete.html', {'post': post} )
