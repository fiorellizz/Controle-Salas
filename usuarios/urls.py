from django.urls import path
from . import views  
urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logar/', views.login, name='login'),
    path('sair/', views.sair, name='sair'),
    path('trocar/', views.cadastro, name='trocar'),
]