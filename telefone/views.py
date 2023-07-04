from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from rest_framework import viewsets, generics, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from telefone.forms import TelefoneForms
from .models import Telefone
from telefone.serializer import TelefoneSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TelefonesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    """Exibindo todos os telefone"""
    queryset = Telefone.objects.order_by('numero_telefone')
    serializer_class = TelefoneSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['numero_telefone']
    search_fields = ['numero_telefone']
    filterset_fields = ['disponibilidade']
    http_method_names = ['get']


class TelefoneViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    """Exibindo telefone"""
    queryset = Telefone.objects.all()
    serializer_class = TelefoneSerializer
    http_method_names = ['get']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        numero_telefone = self.kwargs['numero_telefone']
        return queryset.filter(numero_telefone=numero_telefone)


def telefone(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    lista_telefones = Telefone.objects.order_by("numero_telefone")
    return render(request, 'telefone/telefones.html', {"lista_telefones": lista_telefones})


def editar_telefone(request, id):
    telefone = get_object_or_404(Telefone, id=id)
    if request.method == 'POST':
        form = TelefoneForms(request.POST, instance=telefone)
        if form.is_valid():
            form.save()
            messages.success(request, 'Telefone editado com sucesso!')
            return redirect('telefone')
    else:
        form = TelefoneForms(instance=telefone)
    return render(request, 'telefone/editar_telefone.html', {'form': form, 'id': id})


def deletar_telefone(request, id):
    if request.user.is_authenticated:
        telefone = Telefone.objects.get(id=id)
        telefone.delete()
        messages.success(request, 'Deleção feita com sucesso!')
        return redirect('telefone')


def buscar_telefone(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')

    numero_telefone = request.GET.get('numero_telefone')
    telefone_jovem = request.GET.get('telefone_jovem')
    telefone_responsavel = request.GET.get('telefone_responsavel')

    lista_telefones = Telefone.objects.all()

    if numero_telefone:
        lista_telefones = lista_telefones.filter(numero_telefone=numero_telefone)
    if telefone_jovem:
        lista_telefones = lista_telefones.filter(telefone_jovem=telefone_jovem)
    if telefone_responsavel:
        lista_telefones = lista_telefones.filter(telefone_responsavel=telefone_responsavel)

    return render(request, 'telefone/telefones.html', {"lista_telefones": lista_telefones})

