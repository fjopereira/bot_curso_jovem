from django.db import models


class Interacao(models.Model):
    mensagem = models.TextField()
    ordem = models.FloatField()
    audio = models.CharField(max_length=100, blank=True)
    img = models.CharField(max_length=100, blank=True)
    pdf = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.mensagem
