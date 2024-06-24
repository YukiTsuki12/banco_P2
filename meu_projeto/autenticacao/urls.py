# autenticacao/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('login/', views.login_view, name='login'),  
    path('registrar/', views.registrar, name='registrar'),
    path('logout/', views.logout_view, name='logout'),
    path('listar_carros/', views.listar_carros, name='listar_carros'),
    path('criar_carro/', views.criar_carro, name='criar_carro'),
    path('editar_carro/<int:pk>/', views.editar_carro, name='editar_carro'),
    path('deletar_carro/<int:pk>/', views.deletar_carro, name='deletar_carro'),
    path('chat/', views.chat, name='chat'),
    path('formulario/', views.formulario_view, name='formulario'),
]
