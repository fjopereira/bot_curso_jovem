from django.urls import path, include
from telefone.views import TelefonesViewSet, TelefoneViewSet, telefone, \
                            editar_telefone, deletar_telefone, buscar_telefone
from rest_framework import routers


router = routers.DefaultRouter()
router.register('telefone', TelefonesViewSet, basename='Telefones')


urlpatterns = [
    path('retorna_telefones/', include(router.urls)),
    path('retorna_telefone/<str:numero_telefone>/', TelefoneViewSet.as_view()),

    path('telefone/', telefone, name='telefone'),
    path('editar_telefone/<int:id>/', editar_telefone, name='editar_telefone'),
    path('deletar_telefone/<int:id>/', deletar_telefone, name='deletar_telefone'),
    path('buscar_telefone/', buscar_telefone, name='buscar_telefone'),

]

