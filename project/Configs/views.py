from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.http import Http404

# Create your views here.
@login_required
def update_user_profile(request):
    perfil = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            # Redirigir al home después de actualizar
            return redirect('mi_blog:home')
    else:
        form = UserProfileForm(instance=perfil)

    return render(request, 'config/conf.html', {'form': form})

# Vista para manejar el cambio del dark_mode
@login_required
def change_dark_mode(request):
    perfil = request.user.userprofile
    
    # Verificamos si el usuario ya tiene una configuración de dark_mode
    if perfil is None:
        raise Http404("Perfil no encontrado.")
    
    # Cambiar el valor de dark_mode
    perfil.dark_mode = not perfil.dark_mode  # Cambia el estado de dark_mode
    perfil.save()

    return redirect('mi_blog:home')  # Redirige a la página principal después de aplicar el cambio