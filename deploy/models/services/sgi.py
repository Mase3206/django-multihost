from django.db import models
from .db import Postgres

from .parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)


class Gunicorn(models.Model):
	volumes = models.ManyToManyField(
		Volume,
		related_name='gunicorn'
	)
	networks = models.ManyToManyField(
		Network,
		related_name='gunicorn'
	)
	environment = models.ManyToManyField(
		EnvironmentVariable,
		related_name='gunicorn'
	)
	labels = models.ManyToManyField(
		Label,
		related_name='gunicorn'
	)

	django_project_folder = models.CharField(
		max_length=30, 
		blank=False,
		help_text='Main project folder containing the settings.py file; Ex: django_project, dj, project, etc.'
	)
	database = models.OneToOneField(
		Postgres,
		on_delete=models.DO_NOTHING  # this is only used for sharing the environment variables between the two, such as for db creds
	)