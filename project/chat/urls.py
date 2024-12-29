from django.urls import path
from . import views


app_name = 'mi_chat'

urlpatterns = [
    path('', views.mostrar_chat, name='chat'),
]