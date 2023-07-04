from django.urls import path
from api.views import UserTokenCreateAPIView, generate_token, tela_tokenJWT


urlpatterns = [
    path('api/token/', UserTokenCreateAPIView.as_view(), name='create-token'),
    path('cadatro_token/', generate_token, name='cadatro_token'),
    path('tela_cadatro_tokenJWT/', tela_tokenJWT, name='tela_cadatro_tokenJWT'),


]

