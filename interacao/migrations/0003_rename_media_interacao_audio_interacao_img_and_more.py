# Generated by Django 4.2.2 on 2023-06-27 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interacao', '0002_interacao_media'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interacao',
            old_name='media',
            new_name='audio',
        ),
        migrations.AddField(
            model_name='interacao',
            name='img',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='interacao',
            name='pdf',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
