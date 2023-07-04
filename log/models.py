from django.db import models


class Log(models.Model):
    telefone = models.CharField(max_length=20)
    hora = models.DateTimeField(auto_now=True)
    tipo = models.CharField(max_length=3, choices=[('in', 'Entrada'), ('out', 'Saída')])
    mensagem = models.TextField()

    def __str__(self):
        return self.telefone

