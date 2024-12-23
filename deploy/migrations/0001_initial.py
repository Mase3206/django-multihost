# Generated by Django 5.1.4 on 2024-12-22 01:58

import django.core.validators
import django.db.models.deletion
import pathlib
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentVariable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('[A-Z_]', 'Only uppercase ASCII letters and the underscore character are permitted in environment variable names.')])),
                ('value', models.CharField(blank=True, help_text='This can be empty.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Ex: "traefik.http.routers.gunicorn.rule"', max_length=200)),
                ('value', models.CharField(help_text='Ex: "Host(gunicorn)"', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('external', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_path', models.FilePathField(path=pathlib.PurePosixPath('/Users/noahroberts/GitHub/django-multihost/django_multihost/deploydata/volumes'))),
                ('guest_path', models.CharField(max_length=50)),
                ('mode', models.CharField(choices=[('', 'Read/write (default)'), ('rw', 'Read/write (explicit)'), ('ro', 'Read-only')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Postgres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='pgdb', help_text='Name of the database within Postgres', max_length=40)),
                ('username', models.CharField(default='pguser', help_text='The database username your project will use to connect to Postgres', max_length=30)),
                ('password', models.CharField(default='pgpass', help_text='The password of the database user. Randomly generated passwords (up to 128 chars long) are highly recommended.', max_length=128)),
                ('environment', models.ManyToManyField(related_name='postgres', to='deploy.environmentvariable')),
                ('labels', models.ManyToManyField(related_name='postgres', to='deploy.label')),
                ('networks', models.ManyToManyField(related_name='postgres', to='deploy.network')),
                ('volumes', models.ManyToManyField(related_name='postgres', to='deploy.volume')),
            ],
        ),
        migrations.CreateModel(
            name='Gunicorn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('django_project_folder', models.CharField(help_text='Main project folder containing the settings.py file; Ex: django_project, dj, project, etc.', max_length=30)),
                ('environment', models.ManyToManyField(related_name='gunicorn', to='deploy.environmentvariable')),
                ('labels', models.ManyToManyField(related_name='gunicorn', to='deploy.label')),
                ('networks', models.ManyToManyField(related_name='gunicorn', to='deploy.network')),
                ('database', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='deploy.postgres')),
                ('volumes', models.ManyToManyField(related_name='gunicorn', to='deploy.volume')),
            ],
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('git_repo', models.URLField()),
                ('sgi_server', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deploy.gunicorn')),
                ('database', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='deploy.postgres')),
            ],
        ),
    ]
