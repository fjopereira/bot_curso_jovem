from rest_framework import serializers
from .models import Telefone

class TelefoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Telefone
        fields = ['id',
                  'numero_telefone',
                  'apelido',
                  'nome_jovem',
                  'idade_jovem',
                  'escolaridade',
                  'turno',
                  'telefone_jovem',
                  'nome_responsavel',
                  'telefone_responsavel']

