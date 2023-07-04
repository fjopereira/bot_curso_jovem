from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['telefone', 'tipo', 'formatted_hora', 'mensagem']
    list_filter = ['tipo']
    search_fields = ['telefone']

    ordering = ['-hora']

    def formatted_hora(self, obj):
        return obj.hora.strftime("%d/%m/%Y %H:%M:%S")

    formatted_hora.short_description = 'Hora'