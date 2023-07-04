from django.db import models


class Mensagem(models.Model):
    bot = models.BooleanField(default=True)

    def __str__(self):
        return f"Mensagem {self.pk} - Bot: {self.bot}"

