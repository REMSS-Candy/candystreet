from django.urls import path
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/inventory/login', permanent=False),
         name='inventory_index_login_redir'),
    path('login/', views.user.login_view, name='login'),
    path('logout/', views.user.logout_view, name='logout'),
    path('sell/', views.sell.sell, name='sell')
]
