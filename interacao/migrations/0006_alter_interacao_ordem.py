# Generated by Django 4.2.2 on 2023-06-27 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interacao', '0005_interacao_case_alter_interacao_ordem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interacao',
            name='ordem',
            field=models.FloatField(),
        ),
    ]
