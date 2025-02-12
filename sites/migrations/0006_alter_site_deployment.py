# Generated by Django 5.1.4 on 2024-12-23 07:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0007_deployment_set_on_delete_to_null'),
        ('sites', '0005_remove_site_path_remove_site_remote_repo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='deployment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='site', to='deploy.deployment'),
        ),
    ]
