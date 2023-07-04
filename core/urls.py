from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('controle/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('', include('usuarios.urls')),
    path('', include('interacao.urls')),
    path('', include('log.urls')),
    path('', include('telefone.urls')),
    path('', include('mensagens.urls')),
    path('', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#
# content-type application/json
# {
#   passa o usuário e a senha e recupera um token temporário
#   "username": "api",
#   "password": 123456
#
# }
# Authorization
# Bearer + espaço + key
#refresh
#access