from django.urls import path, include
from . import views


app_name = 'mi_blog'

urlpatterns = [
    path('', views.Mostrar_Post, name='home'),
    path('crear/', views.article_create, name='created'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug_post>/', views.post_detail, name='detalle'),
    path('profile/', views.profile, name='profile'),
    path('perfil/<str:username>/<slug:slug>/', views.mostrar_perfil, name='perfilOne'),
    path('delete-image/', views.delete_profile_image, name='delete_profile_image'),
    path('accounts/login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('<int:post_id>/comment/', views.post_comment, name='comment'),
    path('search/', views.Search, name='search'),
    path('eliminar/<int:post_id>/', views.EliminarPost, name='delete'),
    path('friendships/', include('friends.urls')),
    path('users/', views.mostrar_usuarios, name='lista_usuarios'),
    path('amigos/<str:username>/', views.show_my_friends, name='my_friends'),
    path('like/<int:post_id>/', views.toggle_like, name='likes')
]