# Generated by Django 5.1.4 on 2024-12-24 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0007_deployment_set_on_delete_to_null'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployment',
            name='online',
        ),
    ]