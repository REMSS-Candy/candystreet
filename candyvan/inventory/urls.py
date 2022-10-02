from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user.login, name='login'),
    path('logout/', views.user.logout, name='logout'),
]
