# Generated by Django 4.2.2 on 2023-06-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telefone', '0003_telefone_chave_cadastro_telefone_endereco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telefone',
            name='disponibilidade',
            field=models.BooleanField(default=False),
        ),
    ]
