import string
import random
from django.db import models


class Telefone(models.Model):
    numero_telefone = models.CharField(max_length=20)
    ordem = models.FloatField()

    turno = models.CharField(max_length=50, blank=True)
    apelido = models.CharField(max_length=100, blank=True)
    chave_cadastro = models.CharField(max_length=50, unique=True, blank=True)
    nome_jovem = models.CharField(max_length=100, blank=True)
    idade_jovem = models.CharField(max_length=30, blank=True)
    escolaridade = models.CharField(max_length=50, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    objetivo = models.CharField(max_length=30, blank=True)
    telefone_jovem = models.CharField(max_length=20, blank=True)
    nome_responsavel = models.CharField(max_length=100, blank=True)
    telefone_responsavel = models.CharField(max_length=20, blank=True)
    disponibilidade = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.chave_cadastro:
            self.chave_cadastro = self.gerar_chave_aleatoria()
        super().save(*args, **kwargs)

    def gerar_chave_aleatoria(self):
        caracteres = string.ascii_letters + string.digits
        chave = ''.join(random.choices(caracteres, k=10))
        return chave

    def __str__(self):
        return self.numero_telefone

