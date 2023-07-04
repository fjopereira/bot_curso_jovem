from django.contrib import admin
from .models import Telefone

@admin.register(Telefone)
class TelefoneAdmin(admin.ModelAdmin):
    list_display = ['numero_telefone', 'ordem', 'apelido', 'nome_jovem',
                    'idade_jovem', 'escolaridade', 'turno', 'telefone_jovem',
                    'nome_responsavel', 'telefone_responsavel']
    search_fields = ['numero_telefone', 'telefone_jovem', 'telefone_responsavel',
                     'nome_jovem', 'nome_responsavel', 'chave_cadastro']
    readonly_fields = ['chave_cadastro']
    list_filter = ['turno']
    list_per_page = 100
    ordering = ['numero_telefone']

