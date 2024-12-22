# Generated by Django 5.1.4 on 2024-12-22 03:38

import deploy.models.services.parts
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0003_deployment_modified_deployment_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volume',
            name='host_path',
            field=models.CharField(max_length=255, validators=[deploy.models.services.parts.validate_and_create_path]),
        ),
    ]