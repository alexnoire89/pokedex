from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_usuario, name='login_usuario'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('inicio/', views.inicio, name='inicio'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('pokedex/', views.pokedex, name='pokedex'),
    path('audio-player/', views.audio_player, name='audio_player'),







]
