from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from api.models import Api


class UserTokenCreateAPIView(APIView):
    def post(self, request):
        users = User.objects.all()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return render(request, 'api/cadastro_token.html', {'users': users})

        token = Token.objects.filter(user=user).first()

        if token:
            token = token.key
        else:
            token = Token.objects.create(user=user).key

        try:
            api = Api.objects.get(user=user)
            api.token = token
            api.save()
        except Api.DoesNotExist:
            Api.objects.create(user=user, token=token)

        messages.success(request, 'Token criado')
        return render(request, 'api/cadastro_token.html', {'users': users})


def generate_token(request):
    users = User.objects.all()
    return render(request, 'api/cadastro_token.html', {'users': users})


def tela_tokenJWT(request):
    return render(request, 'api/cadastro_tokenJWT.html')

