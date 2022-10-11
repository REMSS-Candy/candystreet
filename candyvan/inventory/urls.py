from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/inventory/login', permanent=False),
         name='inventory_index_login_redir'),
    path('login/', views.user.login, name='login'),
    path('logout/', views.user.logout, name='logout'),
    path('sell/', views.sell.sell, name='sell')
]
