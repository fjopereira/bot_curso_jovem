# Generated by Django 4.2.2 on 2023-06-27 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interacao', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interacao',
            name='media',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
