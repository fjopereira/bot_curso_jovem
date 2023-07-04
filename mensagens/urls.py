from django.urls import path
from mensagens.views import post_envio, post_entrada


urlpatterns = [
    path('post_envio/', post_envio, name='post_envio'),
    path('post_entrada/', post_entrada, name='post_entrada'),


]

