# Generated by Django 4.2.2 on 2023-06-23 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefone', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telefone',
            old_name='telefone',
            new_name='numero_telefone',
        ),
    ]