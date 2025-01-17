# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notfs'  

urlpatterns = [
    path('notifications/', views.notificatios_views, name='show_notfs')
]