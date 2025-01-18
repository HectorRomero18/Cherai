# urls.py (friends)
from django.urls import path
from . import views

app_name = 'friends'

urlpatterns = [
    path('requests/', views.friend_requests, name='friend_requests'),
    path('send/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept/<str:username>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject/<str:username>/', views.reject_friend_request, name='reject_friend_request'),
    path('delete/<str:username>/', views.delete_friend, name='delete_friend'),
    path('follow/<str:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('show_followers/', views.show_followers, name='my_followers'),
    path('followings/', views.show_my_followings, name='show_my_followings'),
]
