# Generated by Django 5.1.4 on 2024-12-22 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gunicorn',
            options={'verbose_name_plural': 'gunicorn containers'},
        ),
        migrations.AlterModelOptions(
            name='postgres',
            options={'verbose_name_plural': 'postgres containers'},
        ),
    ]
