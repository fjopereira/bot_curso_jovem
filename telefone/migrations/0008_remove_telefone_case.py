# Generated by Django 4.2.2 on 2023-06-27 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefone', '0007_telefone_apelido_telefone_turno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telefone',
            name='case',
        ),
    ]
