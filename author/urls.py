from django.urls import path
from .views import get_authors
from . import views

app_name = 'author'

urlpatterns = [
    path('', views.get_authors, name='get_authors'),
    # 根据 AUTHOR_SERIAL 获取或更新作者信息
    path('<int:pk>/', views.author_profile, name='author_profile'),

    # 根据 AUTHOR_FQID 获取作者信息
    path('fqid/<str:author_fqid>/', views.author_profile_fqid, name='author_profile_fqid'),
    path('register/', views.register, name='register'),
    path('<str:author_serial>/followers/', views.followers_list, name='followers_list'),
    path('<str:author_serial>/followers/<path:foreign_author_fqid>/', views.check_follower, name='check_follower'),
]