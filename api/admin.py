from django.contrib import admin
from .models import Api

@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')

