# Generated by Django 5.1.4 on 2024-12-23 07:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0006_remove_postgres_name_remove_postgres_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployment',
            name='database',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='deploy.postgres'),
        ),
        migrations.AlterField(
            model_name='deployment',
            name='sgi_server',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='deploy.gunicorn', verbose_name='SGI server'),
        ),
    ]
