from django.urls import path
from . import views


app_name = 'mi_blog'

urlpatterns = [
    path('', views.Mostrar_Post, name='home'),
    path('crear/', views.article_create, name='created'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug_post>/', views.post_detail, name='detalle'),
    path('profile/', views.profile, name='profile'),
    path('delete-image/', views.delete_profile_image, name='delete_profile_image'),
    path('accounts/login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
]