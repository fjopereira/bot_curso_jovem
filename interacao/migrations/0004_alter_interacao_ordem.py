# Generated by Django 4.2.2 on 2023-06-27 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interacao', '0003_rename_media_interacao_audio_interacao_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interacao',
            name='ordem',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
