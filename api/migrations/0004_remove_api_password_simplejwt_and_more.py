# Generated by Django 4.2.2 on 2023-06-30 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_api_password_simplejwt_api_username_simplejwt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='api',
            name='password_simplejwt',
        ),
        migrations.RemoveField(
            model_name='api',
            name='username_simplejwt',
        ),
    ]
