from django.urls import path
from .views import get_authors
from . import views

app_name = 'author'

urlpatterns = [

    path('', views.get_authors, name='get_authors'),
    
    path('<str:author_serial>/', views.author_profile, name='author_profile'),

    path('register/', views.register, name='register'),

    path('login/', views.login_view, name='login'),




    path('<str:author_serial>/followers/', views.followers_list, name='followers_list'),
    path('<str:author_serial>/followers/<path:foreign_author_fqid>/', views.check_follower, name='check_follower'),
    path('<str:author_serial>/follow_requests/', views.receive_follow_request, name='receive_follow_request'),
]