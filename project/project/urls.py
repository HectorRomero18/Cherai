"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from mi_blog import views

# Redirigir la página principal a la página de login
def redirect_to_login(request):
    return redirect('account_login')  # Redirige a la vista de login de Allauth


urlpatterns = [
    path('', views.custom_login, name='home'),
    path('blog/', include('mi_blog.urls', namespace='blog')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
# Solo en desarrollo, Django sirve archivos de medios
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
