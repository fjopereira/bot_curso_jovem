from django.contrib import admin
from .models import Mensagem


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ['id', 'bot']

