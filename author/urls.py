from django.urls import path
from .views import get_authors
from . import views

app_name = 'author'

urlpatterns = [
    path('', views.get_authors, name='get_authors'),
    
    path('<int:pk>/', views.author_profile, name='author_profile'),

    
    path('fqid/<str:author_fqid>/', views.author_profile_fqid, name='author_profile_fqid'),
    path('register/', views.register, name='register'),
    path('<str:author_serial>/followers/', views.followers_list, name='followers_list'),
    path('<str:author_serial>/followers/<path:foreign_author_fqid>/', views.check_follower, name='check_follower'),
    path('<str:author_serial>/follow_requests/', views.receive_follow_request, name='receive_follow_request'),
]