from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, User
from datetime import datetime
from django.utils.text import slugify
from .forms import UserProfileForm, UserCreationForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse



# Create your views here.
# Mostrar_Post
@login_required
def Mostrar_Post(request):
    posts = Post.published.all()
    return render(request, 'blog/post/home.html', {'posts': posts})

# article_create
@login_required
def article_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        publish_date = request.POST.get('publish_date')

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
            status=Post.Status.PUBLISHED  # Asignar el estado como PUBLISHED
        )

        # Generar el slug basado en el título
        post.slug = slugify(post.title)
        post.save()  # Guardar el post con el slug generado

        return redirect('mi_blog:home')

    return render(request, 'blog/post/crear.html')

@login_required
def post_detail(request, year, month, day, slug_post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, 
                            slug=slug_post, 
                            publish__year=year, 
                            publish__month=month, 
                            publish__day=day)
    return render(request, 'blog/post/detalles.html', {'post': post} )

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
    return render(request, 'C:/mi_blog/project/mi_blog/templates/account/login.html', {'form': form})

def custom_logout(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('mi_blog:login') 