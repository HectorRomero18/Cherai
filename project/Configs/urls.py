# Configs/urls.py
from django.urls import path
from . import views

app_name = 'configs'  # Nombre del namespace (debe coincidir con el namespace usado en project/urls.py)

urlpatterns = [
    path('settings/', views.update_user_profile, name='config_home'),  
    path('change-dark-mode/', views.change_dark_mode, name='change_dark_mode'),
]
