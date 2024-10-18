from django.urls import path
from .views import get_authors
from . import views


urlpatterns = [

    path('register/', views.register, name='register'),

    path('', views.login_view, name='login'),

]