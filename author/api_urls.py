from django.urls import path
from .views import get_authors
from . import views

app_name = 'author'

urlpatterns = [

    path('', views.get_authors, name='get_authors'),
    
    path('<str:author_serial>/', views.author_profile, name='author_profile'),

    path('<str:author_serial>/followers/', views.get_followers, name='get_followers'),

    path('<str:author_serial>/followers/<path:foreign_author_fqid>/', views.followers_api, name='followers_api'),

]